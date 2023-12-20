"""module for generic dataset implementation"""
from abc import ABC
from typing import Dict, List, Optional


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


class GenericDataset(Dataset, ABC):
    """Generic dataset implementation. This is a flexible dataset for multiple
    use cases. It can be used for classification, segmentation, object detection, etc.
    For specific frameworks, there are subclasses of this class, e.g. KerasGenericDataset
    """

    def __init__(  # noqa: PLR0913
        self,
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
        """
        Constructor of the GenericDataset
        Args:
            set_name: Name of the subset e.g. train
            datainfo_listing: How to list the data
            data_loader: How to load the data
            target_transformer: How to transform the
                target of the model (e.g. one-hot encoding)
            input_transformer: How to transform the input of the model
            shuffle: bool if the data should be shuffled
            data_shuffler: A way of shuffling the data (e.g. random, sampled)
            stats_generator: Write dataset stats
            augmentator: Augment the data on the fly
            net_data_logger: Stores the in the way it is presented to the model
        """
        super().__init__()
        self.net_data_logger = net_data_logger
        self.set_name = set_name
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
        """Initializes the dataset with the data description and context"""
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

    def get_item_count(self) -> int:
        """Returns the current count of items in the dataset"""
        return len(self.data_info_list)

    def get_items_per_epoch(self) -> int:
        """Returns the items per epoch"""
        return len(self.index_list)

    def __getitem__(self, item_index: int):
        """Returns the data of the item at index"""
        real_index = self.index_list[item_index]
        data_info = self.data_info_list[real_index]
        data_item = self.data_loader.load_data(data_info)
        if self.augmentator is not None:
            data_item = self.augmentator(data_item)
        net_inputs = self.input_transformer.get_net_inputs([data_item])
        net_targets = self.target_transformer.get_net_targets([data_item])
        if self.net_data_logger is not None:
            self.net_data_logger.log_data(
                net_inputs=net_inputs,
                net_targets=net_targets,
                data_info_list=[data_info],
            )
        return net_inputs, net_targets

    def get_set_name(self) -> str:
        """Returns the name of the set e.g. train"""
        return self.set_name

    def __len__(self):
        """Returns the number of batches"""
        return self.get_items_per_epoch()

    def get_data_by_key(self, data_key):
        """Returns the data by the key (identifier of the data)"""
        data_info: DataInfo = self.data_info_dict[data_key]
        return self.data_loader.load_data(data_info)

    def get_dataset_stats(self) -> dict:
        """Returns the dataset stats"""
        return self.data_stats_generator.generate_stats(
            self.data_info_list, self.index_list
        )

    def on_epoch_end(self):
        """Shuffles the data if required"""
        if self.shuffle:
            self.index_list = self.data_shuffler.shuffle(self.data_info_list)
