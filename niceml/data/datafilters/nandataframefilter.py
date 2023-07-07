"""Add module for NanDataframeFilter"""
from typing import List

import pandas as pd

from niceml.data.datadescriptions.regdatadescription import RegDataDescription
from niceml.data.datafilters.dataframefilter import DataframeFilter
from niceml.utilities.commonutils import check_instance


class NanDataframeFilter(DataframeFilter):
    """DataframeFilter that removes nan values from feature columns"""

    def filter(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        The filter function is used to remove rows from the data that have NaN values
        in any of the columns that are specified as inputs or targets of the
        `self.data_description`. This is done by dropping all rows where there are NaN
        values in any of these columns.

        Args:
            data: pd.DataFrame: Pass the data into the function

        Returns:
            A dataframe with the rows that have at least one nan value in the columns
            specified by filter_columns removed

        """
        self.data_description: RegDataDescription = check_instance(
            self.data_description, RegDataDescription
        )
        filter_columns: List[str] = []

        for column in self.data_description.inputs + self.data_description.targets:
            filter_columns.append(column["key"])

        return data.dropna(axis=0, subset=filter_columns)
