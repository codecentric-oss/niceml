""" Module for selectboxfilter """
import logging
from typing import List, Optional

import streamlit as st

from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.filters.experimentfilter import ExperimentFilter
from niceml.experiments.metafunctions import MetaFunction

SHOW_ALL_KEY: str = "_all_"


class SelectBoxFilter(ExperimentFilter):
    """Filters experiments for a specific value"""

    def __init__(
        self,
        meta_function: MetaFunction,
        default: Optional[str] = None,
        allow_all: bool = True,
    ):
        self.meta_function = meta_function
        self.selected_value = None
        self.allow_all = allow_all
        self.default = default

    def render(self, exp_list: List[ExperimentData]):
        """
        renders the component in the streamlit sidebar and
        stores the selected result
        """
        values = list(set((self.meta_function(exp) for exp in exp_list)))
        if self.allow_all:
            values = [SHOW_ALL_KEY] + values
        index: int = 0
        if self.default is not None:
            if self.default in values:
                index = values.index(self.default)
            else:
                logging.getLogger(__name__).warning(
                    f"Default cannot be find: {self.default} "
                    f"in {self.meta_function.get_name()}"
                )
        self.selected_value = st.sidebar.selectbox(
            self.meta_function.get_name(), values, index=index
        )

    def filter(self, exp_list: List[ExperimentData]) -> List[ExperimentData]:
        """filters experiments according to the settings"""
        if self.allow_all and self.selected_value == SHOW_ALL_KEY:
            return exp_list
        return [
            exp for exp in exp_list if self.selected_value == self.meta_function(exp)
        ]
