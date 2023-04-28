"""Module for class ExperimentFilter"""
from abc import ABC, abstractmethod
from typing import List

from niceml.experiments.experimentdata import ExperimentData


class ExperimentFilter(ABC):
    """This class allows to filter and render experiments"""

    @abstractmethod
    def render(self, exp_list: List[ExperimentData]):
        """render in streamlit e.g. checkbox or slider"""

    @abstractmethod
    def filter(self, exp_list: List[ExperimentData]) -> List[ExperimentData]:
        """Filters list and returns left over experiments"""
