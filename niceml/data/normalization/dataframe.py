"""Module for dataframe normalization functions"""
from typing import Tuple

import pandas as pd

from niceml.data.normalization.normalization import NormalizationInfo


def normalize_col(
    dataframe: pd.DataFrame, column_key
) -> Tuple[pd.DataFrame, NormalizationInfo]:
    """
    The normalize_col function takes a dataframe and a column key as input.
    It returns the normalized dataframe and the normalization information for that column.
    The normalization is done by subtracting the minimum value from each element in that column,
    and then dividing by (max - min). The offset is equal to min_val, and
    divisor = max_val - min_val.

    Args:
        dataframe: pd.DataFrame: Pass in the dataframe to be normalized
        column_key: Specify which column to normalize

    Returns:
        A tuple of a dataframe and a normalizationinfo object

    """
    min_val = dataframe[column_key].min()
    max_val = dataframe[column_key].max()

    divisor = max_val - min_val

    if divisor == 0:
        raise ZeroDivisionError

    dataframe[column_key] = (dataframe[column_key] - min_val) / divisor

    norm_info = NormalizationInfo(
        feature_key=column_key, offset=float(min_val), divisor=float(divisor)
    )

    return dataframe, norm_info


def denormalize_column(
    norm_info: NormalizationInfo, column: str, data: pd.DataFrame
) -> pd.DataFrame:
    """
    The denormalize_column function takes a `NormalizationInfo` object, a column name, and
    a dataframe as input. It then multiplies the values in the specified column by the divisor
    in the `NormalizationInfo` object and adds to them the offset value from that same object.
    The resulting dataframe is returned.

    Args:
        norm_info: NormalizationInfo: Pass in the `NormalizationInfo` object
        column: str: Specify the column to denormalize
        data: pd.DataFrame: Pass the dataframe to the function

    Returns:
        The dataframe with the column denormalized
    """
    data[column] = data[column] * norm_info.divisor + norm_info.offset
    return data
