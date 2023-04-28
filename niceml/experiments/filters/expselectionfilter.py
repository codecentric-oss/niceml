"""Module for experiment selection filters"""
from typing import List

import streamlit as st

from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.filters.experimentfilter import ExperimentFilter


class ExpCheckboxSelectionFilter(ExperimentFilter):
    """Filters experiments with checkboxes"""

    def __init__(self, default_selected: int = 3):
        self.default_selected = default_selected

    def render(self, exp_list: List[ExperimentData]):
        """Not required because experiments should be filtered at the end"""
        pass

    def filter(self, exp_list: List[ExperimentData]) -> List[ExperimentData]:
        """Filters experiments with checkboxes"""
        exp_out_list: List[ExperimentData] = []
        st.sidebar.markdown("Experiments:")
        for idx, exp_data in enumerate(exp_list):
            if st.sidebar.checkbox(
                exp_format_func(exp_data), value=(idx < self.default_selected)
            ):
                exp_out_list.append(exp_data)
        return exp_out_list


class ExpMultiSelectFilter(ExperimentFilter):
    """Filters experiments with multiselect"""

    def __init__(self, default_selected: int = 3):
        self.default_selected = default_selected

    def render(self, exp_list: List[ExperimentData]):
        """Not required because experiments should be filtered at the end"""
        pass

    def filter(self, exp_list: List[ExperimentData]) -> List[ExperimentData]:
        """Filters experiments with multiselect"""
        id_dict = {exp_format_func(x): x for x in exp_list}
        id_list = list(id_dict.keys())
        default_values = id_list[: self.default_selected]
        selects = st.sidebar.multiselect(
            label="Experiments", options=id_list, default=default_values
        )
        return [id_dict[cur_id] for cur_id in selects]


def exp_format_func(exp_data: ExperimentData) -> str:
    """default formatting for experiments in the dashboard"""
    out_str: str = (
        f"{exp_data.exp_info.experiment_prefix}-"
        f"{exp_data.get_short_id()}-{exp_data.get_run_date().date()}"
    )
    return out_str
