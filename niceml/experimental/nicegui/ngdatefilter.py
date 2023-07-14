from abc import ABC, abstractmethod
from typing import Callable, List
from datetime import date, datetime, timedelta
import json


from nicegui import ui

from niceml.experimental.nicegui.ngfilter import NGExpFilter
from niceml.experiments.experimentdata import ExperimentData


class NGDateFilter(ABC):
    @abstractmethod
    def render(self, exp_list: List[str], on_change) -> None:
        """render datetime input in nicegui"""

    @abstractmethod
    def filter(self, exp_list: List[str]) -> List[str]:
        """Filters list and returns left over experiments"""


class ContainDateFilter(NGExpFilter):
    def __init__(self, days_ago: int = 14, min_shown_exp: int = 5) -> None:
        self.days_ago = days_ago
        self.min_shown_exp = min_shown_exp
        self.selected_values = None
        self.date_selection = None

    def serialize_datetime(self, obj) -> None:
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")

    def render(self, exp_list: List[ExperimentData], on_change: Callable) -> None:
        """Shows the date selection and stores its values"""
        start_date = datetime.today() - timedelta(days=self.days_ago)
        end_date = datetime.today()
        result = ui.label()
        self.date_selection = ui.date(
            # value={'from': start_date, 'to': end_date},
            on_change=on_change
        ).props("range")

    def filter(self, exp_list: List[ExperimentData]) -> List[ExperimentData]:
        """filters the experiments which are inside the selected date range"""
        if self.date_selection.value:
            start_date = datetime.strptime(
                self.date_selection.value["from"], "%Y-%m-%d"
            )
            end_date = datetime.strptime(self.date_selection.value["to"], "%Y-%m-%d")
            date_filtered_list: List[ExperimentData] = []
            not_included_list: List[ExperimentData] = []
            for exp_data in exp_list:
                run_date = exp_data.get_run_date()
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
        return exp_list
