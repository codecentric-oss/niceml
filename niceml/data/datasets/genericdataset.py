from typing import Dict, List, Optional

from tensorflow.keras.utils import Sequence

from niceml.data.augmentation.augmentation import AugmentationProcessor
from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datainfolistings.datainfolisting import DataInfoListing
from niceml.data.datainfos.datainfo import DataInfo
from niceml.data.dataloaders.dataloader import DataLoader
from niceml.data.datasets.dataset import Dataset
from niceml.data.datashuffler.datashuffler import DataShuffler
from niceml.data.datashuffler.defaultshuffler import DefaultDataShuffler
from niceml.data.datastatsgenerator.datastatsgenerator import DataStatsGenerator
from niceml.data.datastatsgenerator.defaultstatsgenerator import DefaultStatsGenerator
from niceml.data.netdataloggers.netdatalogger import NetDataLogger
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.mlcomponents.targettransformer.targettransformer import (
    NetInputTransformer,
    NetTargetTransformer,
)


class GenericDataset(Sequence, Dataset):
    def __init__(
        self,
        batch_size: int,
        set_name: str,
        datainfo_listing: DataInfoListing,
        data_loader: DataLoader,
        target_transformer: NetTargetTransformer,
        input_transformer: NetInputTransformer,
        shuffle: bool,
        data_shuffler: Optional[DataShuffler] = None,
        stats_generator: Optional[DataStatsGenerator] = None,
        augmentator: Optional[AugmentationProcessor] = None,
        net_data_logger: Optional[NetDataLogger] = None,
    ):
        super().__init__()
        self.net_data_logger = net_data_logger
        self.set_name = set_name
        self.batch_size = batch_size
        self.batch_count = None
        self.datainfo_listing: DataInfoListing = datainfo_listing
        self.data_loader: DataLoader = data_loader
        self.shuffle = shuffle
        self.data_shuffler: DataShuffler = data_shuffler or DefaultDataShuffler()
        self.target_transformer: NetTargetTransformer = target_transformer
        self.input_transformer: NetInputTransformer = input_transformer
        self.augmentator: Optional[AugmentationProcessor] = augmentator

        self.data_stats_generator: DataStatsGenerator = (
            stats_generator or DefaultStatsGenerator()
        )

    def initialize(
        self, data_description: DataDescription, exp_context: ExperimentContext
    ):
        self.data_description = data_description

        self.data_loader.initialize(data_description)
        self.data_shuffler.initialize(data_description)
        self.target_transformer.initialize(data_description)
        self.input_transformer.initialize(data_description)
        self.data_info_list: List[DataInfo] = self.datainfo_listing.list(
            data_description
        )
        self.index_list: List[int] = list(range(len(self.data_info_list)))
        self.data_info_dict: Dict[str, DataInfo] = {
            cur_data_info.get_identifier(): cur_data_info
            for cur_data_info in self.data_info_list
        }
        if self.net_data_logger is not None:
            self.net_data_logger.initialize(
                self.data_description, exp_context, self.set_name
            )

        self.on_epoch_end()

    def __getitem__(self, batch_index: int):
        cur_data_infos = self.get_datainfo(batch_index)
        dc_list: list = [self.data_loader.load_data(x) for x in cur_data_infos]
        if self.augmentator is not None:
            dc_list = [self.augmentator(x) for x in dc_list]
        net_inputs = self.input_transformer.get_net_inputs(dc_list)
        net_targets = self.target_transformer.get_net_targets(dc_list)
        if self.net_data_logger is not None:
            self.net_data_logger.log_data(
                net_inputs=net_inputs,
                net_targets=net_targets,
                data_info_list=cur_data_infos,
            )
        return net_inputs, net_targets

    def get_batch_size(self) -> int:
        return self.batch_size

    def get_set_name(self) -> str:
        return self.set_name

    def __len__(self):
        batch_count, rest = divmod(len(self.index_list), self.batch_size)
        if rest > 0:
            batch_count += 1
        if self.batch_count is not None:
            batch_count = min(self.batch_count, batch_count)
        return batch_count

    def get_datainfo(self, batch_index: int) -> List[DataInfo]:
        start_idx = batch_index * self.batch_size
        end_idx = min(len(self.index_list), (batch_index + 1) * self.batch_size)
        data_info_list: List[DataInfo] = []
        for cur_idx in range(start_idx, end_idx):
            real_index = self.index_list[cur_idx]
            image_info = self.data_info_list[real_index]
            data_info_list.append(image_info)
        return data_info_list

    def get_data_by_key(self, data_key):
        data_info: DataInfo = self.data_info_dict[data_key]
        return self.data_loader.load_data(data_info)

    def get_dataset_stats(self) -> dict:
        return self.data_stats_generator.generate_stats(
            self.data_info_list, self.index_list
        )

    def on_epoch_end(self):
        if self.shuffle:
            self.index_list = self.data_shuffler.shuffle(
                self.data_info_list, batch_size=self.batch_size
            )
