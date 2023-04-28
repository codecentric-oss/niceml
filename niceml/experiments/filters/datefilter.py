"""Module for date filter"""
from datetime import date, datetime, timedelta
from typing import List

import streamlit as st

from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.filters.experimentfilter import ExperimentFilter


class DateFilter(ExperimentFilter):
    """Datefilter for selecting experiments"""

    def __init__(self, days_ago: int = 14, min_shown_exp: int = 5):
        self.days_ago = days_ago
        self.selected_values = None
        self.min_shown_exp = min_shown_exp

    def render(self, exp_list: List[ExperimentData]):
        """Shows the date selection and stores its values"""
        start_date = datetime.now() - timedelta(days=self.days_ago)
        end_date = datetime.now()
        self.selected_values = st.sidebar.date_input(
            label="date selection", value=(start_date, end_date)
        )

    def filter(self, exp_list: List[ExperimentData]) -> List[ExperimentData]:
        """filters the experiments which are inside the selected date range"""
        try:
            start_date, end_date = self.selected_values
        except ValueError:
            start_date = self.selected_values[0]
            end_date = date.today()
        date_filtered_list: List[ExperimentData] = []
        not_included_list: List[ExperimentData] = []
        for exp_data in exp_list:
            run_date = exp_data.get_run_date().date()
            if start_date <= run_date <= end_date:
                date_filtered_list.append(exp_data)
            else:
                not_included_list.append(exp_data)
        if len(date_filtered_list) < self.min_shown_exp:
            date_filtered_list += not_included_list[
                : self.min_shown_exp - len(date_filtered_list)
            ]

        date_filtered_list = sorted(
            date_filtered_list, key=lambda x: x.get_run_id(), reverse=True
        )
        return date_filtered_list
