"""Module for TensorDfMetricWrapper"""
import importlib
from os.path import join
from typing import Any, List, Optional

import pandas as pd

from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.mlcomponents.resultanalyzers.dataframes.dfanalyzer import DfMetric
from niceml.mlcomponents.resultanalyzers.tensors.tensormetric import TensorMetric


class TensorDfMetricWrapper(TensorMetric):
    """Wrapper for TensorMetric to include dataframe metrics"""

    def __init__(self, key: str, df_metric_list: List[DfMetric], parquet_filename: str):
        super().__init__(key=key)
        self.df_metric_list = df_metric_list

        if "." in parquet_filename:
            module_name, class_name, filename = parquet_filename.rsplit(".", 2)
            module_name_object = importlib.import_module(module_name)
            parquet_filename = getattr(
                getattr(module_name_object, class_name), filename
            ).value
        if ".parq" not in parquet_filename:
            parquet_filename = f"{parquet_filename}.parq"

        self.parquet_filename = parquet_filename

    def analyse_datapoint(
        self,
        data_key: str,
        data_predicted,
        data_loaded,
        additional_data: dict,
        **kwargs,
    ) -> Optional[Any]:
        """Not required due to dataframe analysis"""

    def get_final_metric(self) -> Optional[dict]:
        """Reads the parquet file and runs the dataframe metrics on it"""
        cur_df: pd.DataFrame = self.exp_context.read_parquet(
            join(
                ExperimentFilenames.ANALYSIS_FOLDER,
                self.parquet_filename.format(subset=self.dataset_name),
            )
        )

        outdict = {}
        for df_metric in self.df_metric_list:
            cur_out_dict = df_metric(cur_df, self.exp_context, self.dataset_name)
            if cur_out_dict is not None:
                outdict.update(cur_out_dict)
        return outdict
