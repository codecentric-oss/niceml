"""Module for DefaultStatsGenerator"""
from typing import List

from niceml.data.datainfos.datainfo import DataInfo
from niceml.data.datastatsgenerator.datastatsgenerator import DataStatsGenerator


class DefaultStatsGenerator(DataStatsGenerator):
    """Default stats generator"""

    def generate_stats(
        self, data_info_list: List[DataInfo], index_list: List[int]
    ) -> dict:
        return dict(data_points=len(data_info_list), used_points=len(index_list))
