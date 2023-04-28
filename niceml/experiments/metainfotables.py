from abc import ABC, abstractmethod
from typing import List, Optional

import pandas as pd

from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.metafunctions import MetaFunction


class MetaTable(ABC):
    @abstractmethod
    def __call__(self, experiments: List[ExperimentData]) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class DefaultMetaTable(MetaTable):
    def __init__(
        self,
        name: str,
        meta_function_list: List[MetaFunction],
        list_functions: Optional[List[str]] = None,
    ):
        self.meta_function_list = meta_function_list
        self.name = name
        self.list_functions = [] if list_functions is None else list_functions

    def get_name(self) -> str:
        return self.name

    def __call__(self, experiments: List[ExperimentData]) -> pd.DataFrame:
        dict_list = list()

        for cur_exp in experiments:
            exp_meta_dict = dict()
            for meta_func in self.meta_function_list:
                info = meta_func(cur_exp)
                func_name = meta_func.get_name()
                if func_name in self.list_functions:
                    if type(info) is not list:
                        info = [info]
                    for col_idx, cur_info in enumerate(info):
                        exp_meta_dict[f"{func_name}_{col_idx:02d}"] = cur_info
                else:
                    exp_meta_dict[func_name] = info
            dict_list.append(exp_meta_dict)

        out_df = pd.DataFrame(dict_list)
        return out_df
