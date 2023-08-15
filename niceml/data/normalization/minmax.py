"""Module for dataframe normalization functions"""
from typing import Tuple

import pandas as pd

from niceml.data.normalization.normalization import (
    NormalizationInfo,
    BinaryNormalizationInfo,
    CategoricalNormalizationInfo,
    ScalarNormalizationInfo,
)


def normalize_scalar_column(
    dataframe: pd.DataFrame, column_key
) -> Tuple[pd.DataFrame, ScalarNormalizationInfo]:
    """
    The normalize_scalar_col function takes a dataframe and a column key as input.
    It returns the normalized dataframe and the normalization information for that column.
    The normalization is done by subtracting the minimum value from each element in that column,
    and then dividing by (max - min). The offset is equal to min_val, and
    divisor = max_val - min_val.

    Args:
        dataframe: pd.DataFrame: Pass in the dataframe to be normalized
        column_key: Specify which column to normalize

    Returns:
        A tuple of the dataframe with the normalized column (`column_key`)
        and a `ScalarNormalizationInfo` object

    """
    min_val = dataframe[column_key].min()
    max_val = dataframe[column_key].max()

    divisor = max_val - min_val

    if divisor == 0:
        divisor = 1

    dataframe[column_key] = (dataframe[column_key] - min_val) / divisor

    norm_info = ScalarNormalizationInfo(
        feature_key=column_key, offset=float(min_val), divisor=float(divisor)
    )

    return dataframe, norm_info


def normalize_binary_column(
    dataframe: pd.DataFrame, column_key: str
) -> Tuple[pd.DataFrame, BinaryNormalizationInfo]:
    """
    The normalize_binary_column function takes a dataframe and the key of a column in
    that dataframe.It then checks to make sure that there are only two unique values
    in the column, and if so, it replaces those values with 0s and 1s. It returns both
    the normalized dataframe and an object containing information about how
    the normalization was performed.

    Args:
        dataframe:  Pass in the dataframe that we want to normalize
        column_key: Specify the column that we want to normalize

    Returns:
        A tuple of the dataframe with the normalized column (`column_key`)
        and a `BinaryNormalizationInfo` object
    """
    values = list(sorted(dataframe[column_key].unique()))
    binary_value_count = 2
    if len(values) > binary_value_count:
        raise ValueError("Binary column must have more than two unique values.")

    dataframe[column_key] = dataframe[column_key].apply(lambda x: values.index(x))

    norm_info = BinaryNormalizationInfo(feature_key=column_key, values=values)
    return dataframe, norm_info


def normalize_categorical_column(
    dataframe: pd.DataFrame, column_key: str
) -> Tuple[pd.DataFrame, CategoricalNormalizationInfo]:
    """
    Normalizes a categorical column in the given DataFrame.

    This function takes a `dataframe` and a `column_key´ representing a categorical
    column. It replaces the categorical values with their corresponding indices
    in a sorted order. The normalization information is also returned.

    Args:
        dataframe: The DataFrame containing the categorical column.
        column_key: The column key of the categorical column to be normalized.

    Returns:
        A tuple containing DataFrame with the normalized column (`column_key`) and a
        CategoricalNormalizationInfo object.
    """

    values = list(sorted(dataframe[column_key].unique()))
    dataframe[column_key] = dataframe[column_key].apply(lambda x: values.index(x))
    norm_info = CategoricalNormalizationInfo(feature_key=column_key, values=values)
    return dataframe, norm_info


def denormalize_column(
    norm_info: NormalizationInfo, data: pd.DataFrame
) -> pd.DataFrame:
    """
    The denormalize_column function takes a `norm_info` of data and denormalizes it.

    Args:
        norm_info: NormalizationInfo: Specify the type of normalization used
        data: pd.DataFrame: Pass in the dataframe that is being normalized

    Returns:
        A pandas dataframe with the column denormalized
    """
    if isinstance(norm_info, ScalarNormalizationInfo):
        data[norm_info.feature_key] = (
            data[norm_info.feature_key] * norm_info.divisor + norm_info.offset
        )
    elif isinstance(norm_info, (BinaryNormalizationInfo, CategoricalNormalizationInfo)):
        data[norm_info.feature_key] = data[norm_info.feature_key].map(
            lambda cur_val: norm_info.values[cur_val]
        )
    else:
        raise NotImplementedError
    return data
