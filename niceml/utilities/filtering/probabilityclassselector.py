"""Module for probability selection"""

from dataclasses import dataclass, field
from typing import List

import pandas as pd


@dataclass
class SelectionInfo:
    """What classes and probability range is included in data"""

    class_set: List[str]
    min_prob_value: float
    max_prob_value: float


@dataclass
class Selection:
    """Specific selection with regard to SelectionInfo"""  # QUEST: better docstring?

    class_name: str
    prob_value: float
    identifiers: List[str] = field(default_factory=lambda: [])


class ProbabilityClassSelector:
    """
    Selection class for a specific dataframe which selects based on a class column
    and a prediction column

    Parameters:
        data: Includes the data to investigate
        class_col: column name containing the classes
        prob_col: column name containing the prediction probabilities
        min_delta: The minimum difference between minimum and maximum probability; default 0.1
    """

    def __init__(
        self,
        data: pd.DataFrame,
        class_col: str,
        prob_col: str,
        min_delta: float = 0.1,
    ):
        self.data = data
        self.class_col = class_col
        self.prob_col = prob_col
        self.min_delta = min_delta

    def get_selection_info(self) -> SelectionInfo:
        """Returns info about the possible selections"""
        class_list = list(self.data[self.class_col].unique())
        min_prob = float(self.data[self.prob_col].min())
        max_prob = float(self.data[self.prob_col].max())
        if max_prob - min_prob < self.min_delta:
            max_prob = min_prob + self.min_delta
        return SelectionInfo(class_list, min_prob, max_prob)

    def get_selected_data(self, selection: Selection):
        """Filter and sort the data due to the selection"""
        selected_data: pd.DataFrame = self.data[
            self.data[self.class_col] == selection.class_name
        ]
        selected_data = selected_data.sort_values(by=[self.prob_col])
        selected_data = selected_data[
            selected_data[self.prob_col] >= selection.prob_value
        ]
        return selected_data
