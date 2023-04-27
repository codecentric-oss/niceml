""" Module for the UniformDistributionShuffler and helper methods"""
from collections import defaultdict
from random import sample, shuffle
from typing import Any, Dict, List

import numpy as np

from niceml.data.datainfos.datainfo import DataInfo
from niceml.data.datashuffler.datashuffler import DataShuffler

MODE_DICT = dict(min=min, max=max, avg=np.mean)


class ModeNotImplementedError(Exception):
    pass


def check_mode(mode: str):
    """Checks if mode is available otherwise raises ModeNotImplementedError"""
    if mode not in MODE_DICT:
        mode_list: str = ",".join(MODE_DICT.keys())
        message: str = f"{mode} not available, please use: {mode_list}"
        raise ModeNotImplementedError(message)


class UniformDistributionShuffler(DataShuffler):
    def __init__(self, class_attr: str, mode: str = "max"):
        """
        A shuffler which generates uniform distributed indexes

        Parameters
        ----------
        class_attr: str
            Classttribute name of the datainfo
        mode: str
            How the target amount of each class should be calculated
            such that they are evenly distributed (max, min, avg)
        """
        check_mode(mode)
        self.class_attr = class_attr
        self.mode = mode

    def shuffle(self, data_infos: List[DataInfo]) -> List[int]:
        class_dict: Dict[str, List] = defaultdict(list)
        for idx, cur_data_info in enumerate(data_infos):
            cur_class = getattr(cur_data_info, self.class_attr)
            class_dict[cur_class].append(idx)

        out_list = classdict_to_indexes(class_dict, self.mode)
        return out_list


def classdict_to_indexes(class_dict: Dict[Any, List[int]], mode: str) -> List[int]:
    """
    Uses the class dict to return a list of indexes

    Parameters
    ----------
    class_dict: Dict[Any, List[int]]
        Contains for each class the list of indexes referring to it
    mode: str
        How the target amount of each class should be calculated
        such that they are evenly distributed (max, min, avg)

    Returns
    -------
        A shuffled list of indexes (each index can occur multiple times)
    """
    check_mode(mode)
    class_count_dict = {x: len(y) for x, y in class_dict.items()}
    cur_mode = MODE_DICT[mode]
    max_count = int(cur_mode(list(class_count_dict.values())))
    out_list: List[int] = []
    for class_list in class_dict.values():
        count, parts = divmod(max_count, len(class_list))
        out_list += class_list * count
        out_list += sample(class_list, parts)
    shuffle(out_list)
    return out_list
