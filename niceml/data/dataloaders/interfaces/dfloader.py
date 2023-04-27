"""Module for abstract dataframe loader"""
from abc import ABC, abstractmethod

import pandas as pd


class DfLoader(ABC):  # pylint: disable=too-few-public-methods
    """Abstract class DfLoader (Dataframe Loader)"""

    @abstractmethod
    def load_df(self, df_path: str) -> pd.DataFrame:
        """Loads and returns the dataframe"""
