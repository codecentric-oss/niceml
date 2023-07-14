"""Module for dfdataset"""
from dataclasses import dataclass
from typing import List, Union, Optional, Any

import numpy as np
import pandas as pd
from tensorflow.keras.utils import (  # pylint: disable=import-error,no-name-in-module
    Sequence,
)

from niceml.data.datadescriptions.regdatadescription import RegDataDescription
from niceml.data.datafilters.dataframefilter import DataframeFilter
from niceml.data.datainfos.datainfo import DataInfo
from niceml.data.dataiterators.dataiterator import DataIterator
from niceml.data.datasets.dataset import Dataset
from niceml.data.datashuffler.datashuffler import DataShuffler
from niceml.data.datashuffler.defaultshuffler import DefaultDataShuffler
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.utilities.commonutils import to_categorical
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_fs_path,
    open_location,
)
from niceml.utilities.ioutils import read_parquet


@dataclass
class RegDataInfo(DataInfo):
    """Datainfo for Regression data"""

    dataid: str
    data: dict

    def get_info_dict(self) -> dict:
        """
        The get_info_dict function returns a dictionary containing the dataid
        and all the data in self.data.

        Returns:
            A dictionary containing the dataid and all the other key-value pairs in self
        """
        info_dict = dict(dataid=self.dataid)
        info_dict.update(self.data)
        return info_dict

    def get_identifier(self) -> str:
        """
        The get_identifier function returns the dataid of this object.

        Returns:
            The dataid
        """
        return self.dataid

    def __getattr__(self, item) -> Any:
        """
        The __getattr__ function is called when an attribute lookup has not found the attribute
        in the usual places (i.e. it is not an instance attribute nor is it
        found in the class tree for self).

        Args:
            item: Access the value of a key in the dictionary

        Returns:
            The value of the key in the data dictionary
        """
        return self.data[item]


class DfDataset(Dataset, Sequence):  # pylint: disable=too-many-instance-attributes
    """Dataset for dataframes"""

    def __init__(  # ruff: noqa: PLR0913
        self,
        id_key: str,
        batch_size: int,
        set_name: str,
        data_location: Union[dict, LocationConfig],
        df_path: str = "{set_name}.parq",
        shuffle: bool = False,
        data_shuffler: Optional[DataShuffler] = None,
        dataframe_filters: Optional[List[DataframeFilter]] = None,
    ):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines all of its attributes.
        The __init__ function takes in a number of arguments, which are used to set up
        these attributes.

        Args:
            id_key: str: Specify the column name of the id column in your dataframe
            batch_size: int: Define the size of each batch
            set_name: str: Identify the dataset
            data_location: Union[dict, LocationConfig]: Specify the location of the data
            df_path: str: Specify the file name of the dataframe
            shuffle: bool: Shuffle the data
            dataframe_filters: Optional[List[DataframeFilter]]: Optional list of dataframe filters
                                to filter the data

        """
        super().__init__()
        self.data_shuffler = data_shuffler or DefaultDataShuffler()
        self.dataframe_filters = dataframe_filters or []
        self.df_path = df_path
        self.data_location = data_location
        self.batch_size = batch_size
        self.set_name = set_name
        self.id_key = id_key
        self.index_list = []
        self.shuffle = shuffle
        self.data: Optional[pd.DataFrame] = None
        self.inputs: List[dict] = []
        self.targets: List[dict] = []

    def initialize(
        self, data_description: RegDataDescription, exp_context: ExperimentContext
    ):
        """
        The initialize function is called when the data set is created.
        It takes in a `RegDataDescription` object, which contains information about the
        inputs and targets of your dataset. The initialize function should also take in an
        `ExperimentContext` object, which contains information about where to find your
        data on disk. The `ExperimentContext` is not used in this class.
        This function should read in all the necessary files from disk and store them as
        attributes on this class instance.

        Args:
            data_description: RegDataDescription: Pass the data description of the dataset
                                to this class
            exp_context: ExperimentContext: Pass the experiment context.
        """
        self.inputs = data_description.inputs
        self.targets = data_description.targets

        with open_location(self.data_location) as (data_fs, data_root):
            data_path = join_fs_path(
                data_fs, data_root, self.df_path.format(set_name=self.set_name)
            )
            self.data = read_parquet(filepath=data_path, file_system=data_fs)

        for df_filter in self.dataframe_filters:
            df_filter.initialize(data_description=data_description)
            self.data = df_filter.filter(data=self.data)

        self.data = self.data.reset_index(drop=True)
        self.index_list = list(range(len(self.data)))

        self.on_epoch_end()

    def get_batch_size(self) -> int:
        """
        The get_batch_size function returns the batch size of the dataset.

        Returns:
            The batch size
        """
        return self.batch_size

    def get_set_name(self) -> str:
        """
        The get_set_name function returns the name of the set.

        Returns:
            The `set_name` attribute
        """
        return self.set_name

    def get_data_from_idx_list(self, index_list: List[int]):
        """returns data with a given `index_list`"""
        input_data = []
        for cur_input in self.inputs:
            cur_data = self.extract_data(index_list, cur_input)
            input_data.append(np.array(cur_data))
        target_data = []
        for cur_target in self.targets:
            cur_data = self.extract_data(index_list, cur_target)
            target_data.append(np.array(cur_data))

        input_array = np.column_stack(input_data)
        target_array = np.column_stack(target_data)
        return input_array, target_array

    def get_data(self, start_idx: int, end_idx: int):
        """loads data between indexes"""
        cur_indexes = self.index_list[start_idx:end_idx]
        return self.get_data_from_idx_list(cur_indexes)

    def get_data_by_key(self, data_key):
        """
        The get_data_by_key function takes a data_key as an argument and returns the row of
        data from the DataFrame that corresponds to that key. The function uses pandas' loc method
        to return a slice of rows from the DataFrame where the value in self.id_key matches
        data_key.

        Args:
            data_key: Identify the data that is being requested

        Returns:
            A dataframe of the rows where the id_key column matches the data_key parameter
        """
        return self.data.loc[self.data[self.id_key] == data_key]

    def get_all_data(self):
        """loads all data"""
        return self.get_data_from_idx_list(self.index_list)

    def extract_data(self, cur_indexes, cur_input):
        """extracts data"""
        cur_key = cur_input["key"]
        cur_data = self.data.iloc[cur_indexes][cur_key]
        if cur_input["type"] == "categorical":
            cur_data = to_categorical(cur_data, cur_input["value_count"])
        return cur_data

    def __getitem__(self, index):
        """
        The __getitem__ function is called when the `DfDataset` is indexed (while training a model).

        Args:
            index: Specify the start index of the batch

        Returns:
            A batch of input data and target data with the batch size `self.batch_size`
        """
        start_idx = index * self.batch_size
        end_idx = min(len(self.index_list), (index + 1) * self.batch_size)
        input_data, target_data = self.get_data(start_idx, end_idx)

        return input_data, target_data

    def __len__(self):
        """
        The __len__ function is used to determine the number of batches in an epoch.

        Returns:
            The number of batches in the dataset
        """
        batch_count, rest = divmod(len(self.index_list), self.batch_size)
        if rest > 0:
            batch_count += 1
        return batch_count

    def on_epoch_end(self):
        """shuffles on epoch end"""
        if self.shuffle:
            self.index_list = self.data_shuffler.shuffle(
                data_infos=self.get_all_data_info()
            )

    def iter_with_info(self):
        """
        The iter_with_info function is a generator that yields the next batch of data,
        along with some additional information about the batch.
        The additional information is useful for various diagnostic purposes.
        The function returns an object of type DataIterator, which has two fields:
            * 'batch' contains the next batch of data.
            * 'info' contains additional information about that batch.

        Returns:
            A dataiterator object
        """
        return DataIterator(self)

    def get_datainfo(self, batch_index):
        """creates datainfo for given index"""
        start_idx = batch_index * self.batch_size
        end_idx = min(len(self.index_list), (batch_index + 1) * self.batch_size)
        data_info_list: List[RegDataInfo] = []
        input_keys = [input_dict["key"] for input_dict in self.inputs]
        target_keys = [target_dict["key"] for target_dict in self.targets]
        data_subset = self.data[[self.id_key] + input_keys + target_keys]
        real_index_list = [self.index_list[idx] for idx in range(start_idx, end_idx)]
        data_info_dicts: List[dict] = data_subset.iloc[real_index_list].to_dict(
            "records"
        )

        for data_info_dict in data_info_dicts:
            key = data_info_dict[self.id_key]
            data_info_dict.pop(self.id_key)
            data_info_list.append(RegDataInfo(key, data_info_dict))
        return data_info_list

    def get_all_data_info(self) -> List[RegDataInfo]:
        """
        The get_all_data_info function returns a list of RegDataInfo objects.
        Each RegDataInfo object contains the following information:
            - key: The unique identifier for each data point
            - input_dict: A dictionary mapping input keys to their values
            - target_dict: A dictionary mapping target keys to their values

        Returns:
            A list of `RegDataInfo` objects

        """
        input_keys = [input_dict["key"] for input_dict in self.inputs]
        target_keys = [target_dict["key"] for target_dict in self.targets]
        data_subset = self.data[[self.id_key] + input_keys + target_keys]
        data_info_dicts: List[dict] = data_subset.to_dict("records")
        data_info_list: List[RegDataInfo] = []
        for data_info_dict in data_info_dicts:
            key = data_info_dict.pop(self.id_key)
            data_info_list.append(RegDataInfo(key, data_info_dict))

        return data_info_list
