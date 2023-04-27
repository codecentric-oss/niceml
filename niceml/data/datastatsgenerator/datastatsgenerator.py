"""Module for DataStatsGenerator"""
from abc import ABC, abstractmethod
from typing import List

from niceml.data.datainfos.datainfo import DataInfo


class DataStatsGenerator(ABC):
    """ABC for generating stats in a dataset"""

    @abstractmethod
    def generate_stats(
        self, data_info_list: List[DataInfo], index_list: List[int]
    ) -> dict:
        """Creates stats from a data_info_list and an index list"""
