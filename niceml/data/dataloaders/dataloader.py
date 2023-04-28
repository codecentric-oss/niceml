"""Module for abstract DataLoader"""
from abc import ABC, abstractmethod
from typing import Any

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datainfos.datainfo import DataInfo


class DataLoader(ABC):
    """Abstract implementation of a data loader which is used by the GenericDataset"""

    def __init__(self):
        self.data_description = None

    @abstractmethod
    def load_data(self, data_info: DataInfo) -> Any:
        """Loads the data from a DataInfo object and puts it in a container class"""

    def initialize(self, data_description: DataDescription):
        """Initializes the DataLoader with a DataDescription"""
        self.data_description: DataDescription = data_description
