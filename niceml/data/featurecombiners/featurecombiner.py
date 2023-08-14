"""Module for feature combiner"""
from abc import ABC, abstractmethod

import pandas as pd


class FeatureCombiner(ABC):
    """FeatureCombiner that can combine column-based features as part
    of a DfDataset to create new features."""

    @abstractmethod
    def combine_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        The combine_features function takes in a dataframe and returns a new dataframe
        with the features combined. The features to be combined must be initialized
        in the `__init__` of the concrete class implementation.

        Args:
            data: pd.DataFrame: Pass in the dataframe that we want to transform

        Returns:
            A dataframe with the new features
        """
