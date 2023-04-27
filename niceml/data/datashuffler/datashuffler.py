"""module for datashuffler"""
from abc import ABC, abstractmethod
from typing import List, Optional

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datainfos.datainfo import DataInfo


class DataShuffler(ABC):
    """Abstract class for data shufflers"""

    def initialize(self, data_description: DataDescription):
        self.data_description = data_description

    @abstractmethod
    def shuffle(
        self, data_infos: List[DataInfo], batch_size: Optional[int] = None
    ) -> List[int]:
        """Returns a list of shuffled indexes"""
        pass
