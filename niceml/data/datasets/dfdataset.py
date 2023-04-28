"""Module for dfdataset"""
import json
import random
from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
from tensorflow.keras.utils import (  # pylint: disable=import-error,no-name-in-module
    Sequence,
)

from niceml.data.datadescriptions.regdatadescription import RegDataDescription
from niceml.data.datainfos.datainfo import DataInfo
from niceml.data.dataiterators.dataiterator import DataIterator
from niceml.data.dataloaders.interfaces.dfloader import DfLoader
from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.utilities.commonutils import to_categorical


@dataclass
class RegDataInfo(DataInfo):
    """Datainfo for Regression data"""

    dataid: str
    data: dict

    def get_info_dict(self) -> dict:
        info_dict = dict(dataid=self.dataid)
        info_dict.update(self.data)
        return info_dict

    def get_identifier(self) -> str:
        return self.dataid


class DfDataset(Dataset, Sequence):  # pylint: disable=too-many-instance-attributes
    """Dataset for dataframes"""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        id_key: str,
        batch_size: int,
        set_name: str,
        df_loader: DfLoader,
        df_path: str,
        shuffle: bool = False,
    ):
        super().__init__()
        self.batch_size = batch_size
        self.set_name = set_name
        self.id_key = id_key
        self.dataframe: pd.DataFrame = df_loader.load_df(df_path)
        self.index_list = list(self.dataframe.index)
        self.shuffle = shuffle
        self.inputs: List[dict] = []
        self.targets: List[dict] = []

    def get_batch_size(self) -> int:
        return self.batch_size

    def get_set_name(self) -> str:
        return self.set_name

    def initialize(
        self, data_description: RegDataDescription, exp_context: ExperimentContext
    ):
        self.inputs = data_description.inputs
        self.targets = data_description.targets
        self.on_epoch_end()

    def get_data_from_idx_list(self, index_list: List[int]):
        """retunrs data with a given indexlist"""
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
        return self.dataframe.loc[self.dataframe[self.id_key] == data_key]

    def get_all_data(self):
        """loads all data"""
        return self.get_data_from_idx_list(self.index_list)

    def extract_data(self, cur_indexes, cur_input):
        """extracts data"""
        cur_key = cur_input["key"]
        cur_data = self.dataframe.loc[cur_indexes, cur_key]
        if cur_input["type"] == "categorical":
            cur_data = to_categorical(cur_data, cur_input["value_count"])
        return cur_data

    def __getitem__(self, index):
        start_idx = index * self.batch_size
        end_idx = min(len(self.index_list), (index + 1) * self.batch_size)
        input_data, target_data = self.get_data(start_idx, end_idx)

        return input_data, target_data

    def __len__(self):
        batch_count, rest = divmod(len(self.index_list), self.batch_size)
        if rest > 0:
            batch_count += 1
        return batch_count

    def on_epoch_end(self):
        """shuffles on epoch end"""
        if self.shuffle:
            random.shuffle(self.index_list)

    def iter_with_info(self):
        return DataIterator(self)

    def get_datainfo(self, batch_index):
        """creates datainfo for given index"""
        start_idx = batch_index * self.batch_size
        end_idx = min(len(self.index_list), (batch_index + 1) * self.batch_size)
        data_info_list: List[RegDataInfo] = []
        for cur_idx in range(start_idx, end_idx):
            real_index = self.index_list[cur_idx]
            data_info_dict = {}
            for cur_data in self.inputs + self.targets:
                data_info_dict[cur_data["key"]] = self.dataframe.loc[
                    real_index, cur_data["key"]
                ]
            cur_id = self.dataframe.loc[real_index, self.id_key]
            data_info_dict = json.loads(json.dumps(data_info_dict))
            data_info_list.append(RegDataInfo(cur_id, data_info_dict))
        return data_info_list
