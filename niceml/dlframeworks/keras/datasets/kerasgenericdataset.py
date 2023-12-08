"""module for the KerasGenericDataset class"""
from typing import List

from keras.utils import Sequence

from niceml.data.datainfos.datainfo import DataInfo
from niceml.data.datasets.genericdataset import GenericDataset


class KerasGenericDataset(GenericDataset, Sequence):
    """Keras implementation of the GenericDataset"""

    def __init__(self, batch_size: int, **kwargs):
        """
        Constructor of the KerasGenericDataset
        Args:
            batch_size: Batch size
            **kwargs: All arguments of the GenericDataset
        """
        super().__init__(**kwargs)
        self.batch_size = batch_size

    def __len__(self):
        """
        The __len__ function is used to determine the number of batches in an epoch.
        Contrary to the __len__ function of the GenericDataset, this function
        returns the number of items per epoch.
        """
        batch_count, rest = divmod(self.get_items_per_epoch(), self.batch_size)
        if rest > 0:
            batch_count += 1
        return batch_count

    def get_datainfo(self, batch_index: int) -> List[DataInfo]:
        """
        Returns the datainfo for the batch at index
        Args:
            batch_index: index of the batch

        Returns:
            List of DataInfo with regard to shuffling
        """
        start_idx = batch_index * self.batch_size
        end_idx = min(len(self.index_list), (batch_index + 1) * self.batch_size)
        data_info_list: List[DataInfo] = []
        for cur_idx in range(start_idx, end_idx):
            real_index = self.index_list[cur_idx]
            image_info = self.data_info_list[real_index]
            data_info_list.append(image_info)
        return data_info_list

    def __getitem__(self, batch_index: int):
        """Returns the data of the batch at index"""
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

    def on_epoch_end(self):
        """Shuffles the data if shuffle is True"""
        if self.shuffle:
            self.index_list = self.data_shuffler.shuffle(
                self.data_info_list, batch_size=self.batch_size
            )
