import logging

from abc import ABC, abstractmethod
from typing import Callable, List, Optional

from niceml.experiments.metafunctions import MetaFunction
from niceml.experiments.experimentdata import ExperimentData

from nicegui import ui


SHOW_ALL_KEY: str = "_all_"

class NGExpFilter(ABC):
    @abstractmethod
    def render(self, exp_list: List[ExperimentData], on_change: Callable) -> None:
        """render in nicegui e.g. checkbox or slider"""

    @abstractmethod
    def filter(self, exp_list: List[ExperimentData]) -> List[ExperimentData]:
        """Filters list and returns left over experiments"""


class ContainFilter(NGExpFilter):
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
        self.cur_selection = None

    def render(self, exp_list: List[ExperimentData], on_change: Callable):
        values = list(set((self.meta_function(exp) for exp in exp_list)))
        if self.allow_all:
            values = [SHOW_ALL_KEY] + values
        index: int = 0
        if self.default is not None:
            if self.default in values:
                index = values.index(self.default)
            else:
                logging.getLogger(__name__).warning(
                    f"Default cannot be found: {self.default} "
                    f"in {self.meta_function.get_name()}"
                )

        self.cur_selection = ui.select(
            values,
            label=self.meta_function.get_name(),
            value=values[0],
            on_change=on_change,
        )

    def filter(self, exp_list: List[ExperimentData]) -> List[ExperimentData]:
        if self.allow_all and self.cur_selection.value == SHOW_ALL_KEY:
            return exp_list
        return [
            exp for exp in exp_list if self.cur_selection.value == self.meta_function(exp)
        ]


class NGFilterManager:
    def __init__(self, exp_filters: List[NGExpFilter]):
        self.exp_filters = exp_filters
        self.on_change_callback = None
        self.exp_list = None

    def initialise(self, on_change_callback):
        self.on_change_callback = on_change_callback

    def render(self, exp_list: List[ExperimentData]):
        self.exp_list = exp_list[:]
        for exp_filter in self.exp_filters:
            exp_filter.render(self.exp_list, self.on_change)
    def on_change(self):
        exp_list = self.exp_list[:]
        for exp_filter in self.exp_filters:
            exp_list = exp_filter.filter(exp_list)
        self.on_change_callback(exp_list)

