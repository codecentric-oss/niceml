"""Module for dataset"""
from abc import ABC, abstractmethod
from typing import Iterable, List

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datainfos.datainfo import DataInfo
from niceml.data.dataiterators.dataiterator import DataIterator
from niceml.experiments.experimentcontext import ExperimentContext


class Dataset(ABC):
    """Dataset to load, transform, shuffle the data before training"""

    @abstractmethod
    def get_batch_size(self) -> int:
        """Returns the current batch size"""

    @abstractmethod
    def get_set_name(self) -> str:
        """Returns the name of the set e.g. train"""

    @abstractmethod
    def initialize(
        self, data_description: DataDescription, exp_context: ExperimentContext
    ):
        """Initializes with the data description and context"""

    def iter_with_info(self) -> Iterable:
        """Iterates over the dataset and adds the data_info to each data"""
        return DataIterator(self)

    @abstractmethod
    def __getitem__(self, index: int):
        pass

    @abstractmethod
    def get_datainfo(self, batch_index: int) -> List[DataInfo]:
        """returns the datainfo for the batch at index"""

    @abstractmethod
    def __len__(self):
        pass

    def get_dataset_stats(self) -> dict:
        """Returns the dataset stats"""
        return dict(size=len(self) * self.get_batch_size())

    @abstractmethod
    def get_data_by_key(self, data_key):
        """Returns the data by the key (identifier of the data)"""
