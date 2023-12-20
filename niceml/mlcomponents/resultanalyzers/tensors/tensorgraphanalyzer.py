"""Module for tensorgraphanalyzer"""
from collections import defaultdict
from os.path import join
from typing import List

import mlflow

from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.mlcomponents.resultanalyzers.analyzer import ResultAnalyzer
from niceml.mlcomponents.resultanalyzers.tensors.tensordataiterators import (
    TensordataIterator,
)
from niceml.mlcomponents.resultanalyzers.tensors.tensormetric import TensorMetric
from niceml.utilities.fsspec.locationutils import open_location


class TensorGraphAnalyzer(ResultAnalyzer):
    """Resultanalyzer for analyzing datapoints seperately. Results
    from a previous applied TensorMetric are accessible in the following
    TensorMetrics. For access the `key` attribute is used in each tensormetric."""

    def __init__(
        self,
        metrics: List[TensorMetric],
        dataiterator: TensordataIterator,
        zarr_file_prefix: str = "",
    ):
        """Initializes the TensorGraphAnalyzer"""
        super().__init__()
        self.zarr_file_prefix = zarr_file_prefix
        self.df_metrics: List[TensorMetric] = metrics
        self.dataiterator: TensordataIterator = dataiterator

    def __call__(
        self, dataset: Dataset, exp_context: ExperimentContext, dataset_name: str
    ):  # pylint: disable=too-many-locals
        """Analyzes the dataset with the given metrics"""
        with open_location(exp_context.fs_config) as (exp_fs, exp_root):
            input_file: str = join(
                exp_root,
                ExperimentFilenames.PREDICTION_FOLDER,
                f"{self.zarr_file_prefix}{dataset_name}",
            )
            self.dataiterator.open(input_file, file_system=exp_fs)

        cur_metric: TensorMetric
        for cur_metric in self.df_metrics:
            cur_metric.initialize(
                data_description=self.data_description,
                exp_context=exp_context,
                dataset_name=dataset_name,
            )
            cur_metric.start_analysis()

        for data_key in self.dataiterator:
            cur_data: dict = {}
            data_predicted = self.dataiterator[data_key]
            data_loaded = dataset.get_data_by_key(data_key)
            for cur_metric in self.df_metrics:
                ret_value = cur_metric.analyse_datapoint(
                    data_key, data_predicted, data_loaded, cur_data
                )
                if ret_value is not None:
                    cur_data[cur_metric.key] = ret_value

        out_dict = {}
        for cur_met in self.df_metrics:
            final_metric = cur_met.get_final_metric()
            if final_metric is not None:
                out_dict.update(final_metric)

        output_file = join(
            ExperimentFilenames.ANALYSIS_FOLDER,
            ExperimentFilenames.ANALYSIS_FILE.format(subset_name=dataset_name),
        )
        mlflow_metrics_dict = metrics_dict_to_mlflow_metrics_dict(metrics_dict=out_dict)
        mlflow.log_metrics(mlflow_metrics_dict)
        exp_context.write_yaml(out_dict, output_file)


def metrics_dict_to_mlflow_metrics_dict(metrics_dict: dict) -> dict:
    """
    Converts a nested metrics dictionary to a flat dictionary suitable
    for MLflow logging.

    Args:
        metrics_dict: A dictionary containing metrics, possibly nested.

    Returns:
        dict: A flat dictionary suitable for logging metrics in MLflow.

    Raises:
        ValueError: If a metric is not of type float, dict or list.

    Example:
        Given the input metrics_dict:
        {
            'accuracy': 0.85,
            'precision': {
                'class_0': 0.90,
                'class_1': 0.78
            },
            'loss': [0.5, 0.3, 0.2],
            'confusion_matrix': [
                [50, 5],
                [10, 80]
            ]
        }

        The output mlflow_metrics_dict will be:
        {
            'accuracy': 0.85,
            'precision_class_0': 0.90,
            'precision_class_1': 0.78,
            'loss_0': 0.5,
            'loss_1': 0.3,
            'loss_2': 0.2,
            'confusion_matrix_0_0': 50.0,
            'confusion_matrix_0_1': 5.0,
            'confusion_matrix_1_0': 10.0,
            'confusion_matrix_1_1': 80.0
        }
    """
    mlflow_metrics_dict = defaultdict(float)

    for key, metric in metrics_dict.items():
        try:
            if isinstance(metric, (float, int)):
                mlflow_metrics_dict[key] = float(metric)
            elif isinstance(metric, tuple):
                mlflow_metrics_dict[f"{key}_0"] = float(metric[0])
                mlflow_metrics_dict[f"{key}_1"] = float(metric[1])
            elif isinstance(metric, dict):
                for metric_key, metric_value in metric.items():
                    mlflow_metrics_dict[f"{key}_{metric_key}"] = float(metric_value)
            elif isinstance(metric, list):
                for idx, metric_value in enumerate(metric):
                    if isinstance(metric_value, list):
                        for inner_idx, inner_metric_value in enumerate(metric_value):
                            mlflow_metrics_dict[f"{key}_{idx}_{inner_idx}"] = float(
                                inner_metric_value
                            )
                        continue
                    mlflow_metrics_dict[f"{key}_{idx}"] = float(metric_value)
            else:
                raise ValueError(
                    f"Metric ({key}) should be of type int, float, dict, tuple, or list."
                )
        except (ValueError, TypeError) as error:
            raise TypeError(
                f"Metrics ({key}) of type dict, tuple or list must have values that "
                f"can be parsed to float."
            ) from error
    return mlflow_metrics_dict
