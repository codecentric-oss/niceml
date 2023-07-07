"""Module for tensorgraphanalyzer"""
from os.path import join
from typing import List

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
            ExperimentFilenames.ANALYSIS_FILE.format(dataset_name=dataset_name),
        )
        exp_context.write_yaml(out_dict, output_file)
