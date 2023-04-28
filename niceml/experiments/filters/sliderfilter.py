"""Module contains the filter with a slider"""
from typing import Any, List, Optional

import streamlit as st

from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.filters.experimentfilter import ExperimentFilter
from niceml.experiments.metafunctions import EpochsExtractor, MetaFunction

MODE_STR: List[str] = ["min", "max", "range"]


class UnsupportedModeError(Exception):
    """Error when the mode is not supported"""

    pass


class SliderFilter(ExperimentFilter):
    """Filter for experiments which uses a slider"""

    def __init__(
        self,
        meta_function: MetaFunction,
        default_min: Optional[Any] = None,
        default_max: Optional[Any] = None,
        mode: str = "min",
    ):
        super().__init__()
        self.meta_function = meta_function
        self.default_min = default_min
        self.default_max = default_max
        self.mode = mode
        self.selected_value = None
        if self.mode not in MODE_STR:
            raise UnsupportedModeError(
                f"Mode: {self.mode}" f"is not supported!" f"Supported modes: {MODE_STR}"
            )

    def render(self, exp_list: List[ExperimentData]):
        """renders the component in the streamlit sidebar
        and stores the selected result"""
        values = [self.meta_function(exp_data) for exp_data in exp_list]
        min_value = min(values)
        if self.default_min is not None:
            min_value = min(min_value, self.default_min)
        max_value = max(values)
        if self.default_max is not None:
            max_value = max(max_value, self.default_max)
        if self.mode == MODE_STR[0]:
            value = min_value
        elif self.mode == MODE_STR[1]:
            value = max_value
        else:
            value = (min_value, max_value)
        self.selected_value = st.sidebar.slider(
            label=self.meta_function.get_name(),
            min_value=min_value,
            max_value=max_value,
            value=value,
        )

    def filter(self, exp_list: List[ExperimentData]) -> List[ExperimentData]:
        """filters experiments according to the settings"""
        out_exp_list: List[ExperimentData] = []
        for exp_data in exp_list:
            val = self.meta_function(exp_data)
            if self.mode == MODE_STR[0] and self.selected_value <= val:
                out_exp_list.append(exp_data)
            elif self.mode == MODE_STR[1] and self.selected_value >= val:
                out_exp_list.append(exp_data)
            elif self.mode == MODE_STR[2]:
                sel_min, sel_max = self.selected_value
                if sel_min <= val <= sel_max:
                    out_exp_list.append(exp_data)

        return out_exp_list


def epoch_slider_factory() -> SliderFilter:
    return SliderFilter(
        meta_function=EpochsExtractor(),
        default_min=0,
        default_max=10,
    )
