"""Module for abstract dataframe filter"""
from abc import ABC, abstractmethod

import pandas as pd

from niceml.data.datadescriptions.datadescription import DataDescription


class DataframeFilter(ABC):
    """Filter to filter data of a dataframe"""

    def __init__(self):
        """Filter to filter data of a dataframe"""

        self.data_description = None

    def initialize(self, data_description: DataDescription):
        """
        The initialize function is called once at the beginning of a run.
        It can be used to set up any data structures that are needed for the rest of the run.
        The initialize function takes one argument, which is a data description containing
        information about what data will be available during this run.

        Args:
            data_description: DataDescription: Describe the data that is being passed into the model
        """

        self.data_description = data_description

    @abstractmethod
    def filter(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        The filter function takes a dataframe and returns a filtered version of the
        dataframe. The filter function should return the
        filtered data.

        Args:
            data: pd.DataFrame: Pass the data to be filtered

        Returns:
            A dataframe with the same columns as data, but only containing rows where the
            filter condition is true

        """
