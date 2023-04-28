"""Module for DataframeAnalyzer and DfMetric"""
import logging
from abc import ABC, abstractmethod
from os.path import basename, join
from typing import List

import pandas as pd

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.mlcomponents.resultanalyzers.analyzer import ResultAnalyzer
from niceml.utilities.logutils import get_logstr_from_dict


class DfMetric(ABC):
    """metric of a dataframe"""

    def initialize(self, data_description: DataDescription):
        """Initializes the metric with a data_description"""
        self.data_description = data_description

    @abstractmethod
    def __call__(
        self, data: pd.DataFrame, exp_context: ExperimentContext, dataset_name: str
    ) -> dict:
        """Calculates the metric for the given data and returns a dict with the results"""


class DataframeAnalyzer(ResultAnalyzer):
    """Resultanalyzer for dataframes"""

    def __init__(
        self,
        metrics: List[DfMetric],
        parq_file_prefix: str = "",
    ):
        super().__init__()
        self.parq_file_prefix = parq_file_prefix
        self.df_metrics: List[DfMetric] = metrics

    def initialize(self, data_description: DataDescription):
        super().initialize(data_description)
        for cur_metric in self.df_metrics:
            cur_metric.initialize(data_description)

    def __call__(self, dataset, exp_context: ExperimentContext, dataset_name: str):
        input_file: str = join(
            ExperimentFilenames.PREDICTION_FOLDER,
            f"{self.parq_file_prefix}{dataset_name}.parq",
        )
        data_frame = exp_context.read_parquet(input_file)

        output_file = join(
            ExperimentFilenames.ANALYSIS_FOLDER,
            ExperimentFilenames.ANALYSIS_FILE.format(dataset_name=dataset_name),
        )

        out_dict = {}
        for met in self.df_metrics:
            out_dict.update(met(data_frame, exp_context, dataset_name))

        log_str = f"{basename(output_file)}\n" f"========================\n"

        log_str += get_logstr_from_dict(out_dict)
        logging.getLogger(__name__).info(log_str)

        exp_context.write_yaml(out_dict, output_file)
