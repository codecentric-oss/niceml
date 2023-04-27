"""Module for datainfolisting"""
from abc import ABC, abstractmethod
from typing import List

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datainfos.datainfo import DataInfo


class DataInfoListing(ABC):
    """Abstract class for a data info listing which is used in the GenericDataSet"""

    @abstractmethod
    def list(self, data_description: DataDescription) -> List[DataInfo]:
        """List all data infos for the given data description"""
