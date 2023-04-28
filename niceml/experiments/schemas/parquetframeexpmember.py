"""Module for parquetexpmember"""
from typing import Optional

import pandas as pd
import pandera as pa

from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.schemas.expmember import ExpMember


class ParquetMember(ExpMember):
    """parquet-file which is member of the experiment"""

    def __init__(
        self,
        path: str,
        required: bool,
        description: str,
        df_schema: Optional[pa.DataFrameSchema] = None,
    ):
        super().__init__(
            path=path,
            required=required,
            description=description,
            member_type="parquet-file",
        )
        self.df_schema: Optional[pa.DataFrameSchema] = df_schema

    def validate(self, exp_data: ExperimentData) -> bool:
        result = super().validate(exp_data)
        val_data = exp_data.load_df(self.path)
        val_result = self._validate_schema(val_data)
        return result and val_result

    def _validate_schema(self, val_data: pd.DataFrame) -> bool:
        if self.df_schema is None:
            return True
        try:
            self.df_schema(val_data)
        except pa.errors.SchemaError:
            return False
        return True
