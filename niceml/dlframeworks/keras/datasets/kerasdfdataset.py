"""module for the KerasDfDataset class"""
from typing import List

from niceml.data.datasets.dfdataset import DfDataset, RegDataInfo

from keras.utils import Sequence


class KerasDfDataset(DfDataset, Sequence):
    """Keras implementation of the DfDataset"""

    def __init__(self, batch_size: int, *args, **kwargs):
        """
        Constructor of the KerasdfDataset
        Args:
            batch_size: Batch size
            **kwargs: All arguments of the DfDataset
        """
        super().__init__(*args, **kwargs)
        self.batch_size = batch_size

    def __len__(self):
        """
        The __len__ function is used to determine the number of batches in an epoch.

        Returns:
            The number of batches in an epoch
        """
        batch_count, rest = divmod(self.get_items_per_epoch(), self.batch_size)
        if rest > 0:
            batch_count += 1
        return batch_count

    def __getitem__(self, index):
        """
        The __getitem__ function returns the indexed data batch in the size of `self.batch_size`.
        It is called when the DfDataset is accessed, using the notation self[`index`]
        (while training a model).

         Args:
             index: Specify `index` of the batch

         Returns:
             A batch of input data and target data with the batch size `self.batch_size`
        """
        start_idx = index * self.batch_size
        end_idx = min(len(self.index_list), (index + 1) * self.batch_size)
        input_data, target_data = self.get_data(start_idx, end_idx)

        return input_data, target_data

    def on_epoch_end(self):
        """
        Execute logic to be performed at the end of an epoch (e.g. shuffling the data)
        """
        if self.shuffle:
            self.index_list = self.data_shuffler.shuffle(
                data_infos=self.get_all_data_info(), batch_size=self.batch_size
            )

    def get_datainfo(self, batch_index) -> List[RegDataInfo]:
        """
        The get_datainfo function is used to get the data information for a given batch.

        Args:
            batch_index: Determine which batch of data (datainfo) to return

        Returns:
            A list of `RegDataInfo` objects of the batch with index `batch_index`
        """
        start_idx = batch_index * self.batch_size
        end_idx = min(len(self.index_list), (batch_index + 1) * self.batch_size)
        data_info_list: List[RegDataInfo] = []
        input_keys = [input_dict["key"] for input_dict in self.inputs]
        target_keys = [target_dict["key"] for target_dict in self.targets]
        data_subset = self.data[
            [self.id_key] + input_keys + target_keys + self.extra_key_list
        ]
        real_index_list = [self.index_list[idx] for idx in range(start_idx, end_idx)]
        data_info_dicts: List[dict] = data_subset.iloc[real_index_list].to_dict(
            "records"
        )

        for data_info_dict in data_info_dicts:
            key = data_info_dict[self.id_key]
            data_info_dict.pop(self.id_key)
            data_info_list.append(RegDataInfo(key, data_info_dict))
        return data_info_list

    def get_batch_size(self) -> int:
        """
        The get_batch_size function returns the batch size of the dataset.

        Returns:
            The batch size
        """
        return self.batch_size
