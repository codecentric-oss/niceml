"""Module for DataframeAnalyzer and DfMetric"""

import logging
from abc import ABC, abstractmethod
from os.path import basename, join
from typing import List, Optional

import mlflow
import pandas as pd

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.mlcomponents.resultanalyzers.analyzer import ResultAnalyzer
from niceml.utilities.logutils import get_logstr_from_dict


class DfMetric(ABC):
    """metric of a dataframe"""

    def __init__(self):
        """Initializes a DfMetric and set the data_description attribute to None."""
        self.data_description: Optional[DataDescription] = None

    def initialize(self, data_description: DataDescription):
        """Initializes the metric with a data_description"""
        self.data_description = data_description

    @abstractmethod
    def __call__(
        self, data: pd.DataFrame, exp_context: ExperimentContext, dataset_name: str
    ) -> dict:
        """Calculates the metric for the given data and returns a dict with the results"""


class DataframeAnalyzer(ResultAnalyzer):
    """Result analyzer for dataframes"""

    def __init__(
        self,
        metrics: List[DfMetric],
        parq_file_prefix: str = "",
    ):
        """Initialize a result analyzer for dataframes"""

        super().__init__()
        self.parq_file_prefix = parq_file_prefix
        self.df_metrics: List[DfMetric] = metrics
        self.experiment_context = None

    def initialize(
        self,
        *args,
        data_description: DataDescription,
        exp_context: Optional[ExperimentContext] = None,
        **kwargs,
    ):
        """
        The initialize function initialized the metrics in `self.metrics`
        This function is called once before the first call to the
        evaluate function. It can be used to initialize any variables that are needed
        for evaluation.

        Args:
            *args: Additional arguments that can be added to the ResultAnalyzer
            data_description:   DataDescription that is used by the ResultAnalyzer (available in the
                                `__call__` method). The data_description parameter contains
                                information about the data set, such as number of classes and
                                feature names.
            exp_context:    For some ResultAnalyzers
                            it may be necessary to obtain the experiment context before calling
                            the ResultAnalyzer (`__call__`).
            **kwargs: Additional keyword arguments that can be added to the ResultAnalyzer
        """
        super().initialize(data_description=data_description)
        self.experiment_context = exp_context
        for cur_metric in self.df_metrics:
            cur_metric.initialize(data_description)

    def __call__(self, dataset, exp_context: ExperimentContext, subset_name: str):
        """
        Calculate values of the metrics in `self.metrics` and save them into a csv file.

        Args:
            dataset: Dataset of the experiment. Not used in this function
            exp_context: Current `ExperimentContext` to read and write files
            subset_name: Name the subset

        """
        input_file: str = join(
            ExperimentFilenames.PREDICTION_FOLDER,
            f"{self.parq_file_prefix}{subset_name}.parq",
        )
        data_frame = exp_context.read_parquet(input_file)

        output_file = join(
            ExperimentFilenames.ANALYSIS_FOLDER,
            ExperimentFilenames.ANALYSIS_FILE.format(subset_name=subset_name),
        )

        out_dict = {}
        for met in self.df_metrics:
            out_dict.update(met(data_frame, exp_context, subset_name))

        log_str = f"{basename(output_file)}\n" f"========================\n"

        log_str += get_logstr_from_dict(out_dict)
        logging.getLogger(__name__).info(log_str)

        mlflow.log_dict(out_dict, output_file)
        exp_context.write_yaml(out_dict, output_file)
