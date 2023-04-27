"""Module for regression metric"""
from typing import Callable, Dict, Union

import pandas as pd
from sklearn.metrics import (
    max_error,
    mean_absolute_error,
    mean_squared_error,
    median_absolute_error,
    r2_score,
)

from niceml.experiments.experimentcontext import ExperimentContext
from niceml.mlcomponents.resultanalyzers.dataframes.dfanalyzer import DfMetric

metric_dict = dict(
    mae=mean_absolute_error,
    mse=mean_squared_error,
    r2=r2_score,
    median_absolute_error=median_absolute_error,
    max_error=max_error,
)


class RegMetric(DfMetric):  # pylint: disable = too-many-arguments
    """Regression metric for dataframes"""

    def __init__(  # pylint: disable = too-many-arguments
        self,
        source_col: str,
        target_col: str,
        function_name: str,
        function: Union[str, Callable],
        normalization_file: str = "external_infos/normalization_info.yml",
    ):
        """
        This class let's you calculate arbitrary
        regression metrics. It could be integrated
        as DfMetric in the DataframeAnalyzer(ResultAnalyzer).

        Parameters
        ----------
        source_col: str
            column name in the dataframe where the ground truth is stored.
        target_col: str
            column name where the predictions are stored
        function: str or dict
            function to calculate the metric.
            If str is given it must be a key of the metric dict.
            Otherwise the given dict is initialized with `init_object`
             and additional the key `name`
            must be available to define the
            output name in the result dict.
        function_name: str
            Name of the function
        normalization_file: str, default "normalization_info.yml"
            This is a image_location relative to the experiment
            output folder. If a key exists with the same
            name as `source_col` the metric result is
            normalized and additionaly stored.
        """
        self.source_col = source_col
        self.target_col = target_col
        self.normalization_file: str = normalization_file
        self.func_name = function_name
        if isinstance(function, str):
            try:
                self.function = metric_dict[function]
            except KeyError as error:
                raise Exception(
                    f"Function with name {function}"
                    f" not supported! Available: {list(metric_dict.keys())}"
                ) from error
        else:
            self.function = function

    def __call__(
        self, data: pd.DataFrame, exp_context: ExperimentContext, dataset_name: str
    ) -> dict:
        value = float(self.function(data[self.source_col], data[self.target_col]))
        out_dict = {self.func_name: value}
        try:
            norm_data = exp_context.read_yaml(self.normalization_file)
            norm_data_dict: Dict[str, float] = {
                x["feature_key"]: x["divisor"] for x in norm_data
            }
            if self.source_col in norm_data_dict:
                value_normalized = value * norm_data_dict[self.source_col]
                out_dict[f"{self.func_name}_normalized"] = value_normalized
        except FileNotFoundError:
            pass

        return out_dict
