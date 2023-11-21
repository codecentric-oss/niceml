from nicegui import ui
from typing import Any, Callable, List, Optional

from abc import ABC, abstractmethod

from niceml.experimental.nicegui.ngfilter import NGExpFilter
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.metafunctions import EpochsExtractor, MetaFunction

MODE_STR: List[str] = ["min", "max", "range"]


class UnsupportedModeError(Exception):
    """Error when the mode is not supported"""

    pass


class NGSliderFilter(ABC):
    @abstractmethod
    def render(self, exp_list: List[ExperimentData], on_change: Callable):
        """render in nicegui e.g. checkbox or slider"""

    @abstractmethod
    def filter(self, exp_list: List[ExperimentData]) -> List[ExperimentData]:
        """Filters list and returns left over experiments"""


class ContainSliderFilter(NGExpFilter):
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

    def render(self, exp_list: List[ExperimentData], on_change: Callable) -> None:
        """renders the component in the nicegui sidebar
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

        with ui.row().classes("w-full justify-between"):
            ui.label(self.meta_function.get_name())
            self.container = ui.column()

        def change():
            on_change()
            self.container.clear()
            with self.container:
                ui.label().bind_text_from(self.selected_value, "value")

        self.selected_value = ui.slider(
            min=min_value, max=max_value, value=value, on_change=change
        )

    def filter(self, exp_list: List[ExperimentData]) -> List[ExperimentData]:
        """filters experiments according to the settings"""
        out_exp_list: List[ExperimentData] = []
        for exp_data in exp_list:
            val = self.meta_function(exp_data)
            if self.mode == MODE_STR[0] and self.selected_value.value <= val:
                out_exp_list.append(exp_data)
            elif self.mode == MODE_STR[1] and self.selected_value.value >= val:
                out_exp_list.append(exp_data)
            elif self.mode == MODE_STR[2]:
                sel_min, sel_max = self.selected_value.value
                if sel_min <= val <= sel_max:
                    out_exp_list.append(exp_data)
        return out_exp_list
