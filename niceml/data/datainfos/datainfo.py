"""module for datainfo class"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class DataInfo(ABC):
    """Abstract class for a data info which is used in the GenericDataSet"""

    @abstractmethod
    def get_identifier(self) -> str:
        """Returns the unique identifier for the data info"""

    @abstractmethod
    def get_info_dict(self) -> dict:
        """Returns a dict with all information of the data info"""
