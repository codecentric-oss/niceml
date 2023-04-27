"""Module for TensorMetric"""
from abc import ABC, abstractmethod
from typing import Any, Optional

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.experiments.experimentcontext import ExperimentContext


class TensorMetric(ABC):
    """The tensormetric is used in the tensorgraphanalyzer"""

    def __init__(self, key: str):
        self.output_folder = None
        self.dataset_name = None
        self.data_description = None
        self.exp_context = None
        self.key = key

    def initialize(
        self,
        data_description: DataDescription,
        exp_context: ExperimentContext,
        dataset_name: str,
    ):
        """required parameters for initialization"""
        self.data_description = data_description
        self.exp_context = exp_context
        self.dataset_name = dataset_name

    def start_analysis(self):
        """everything that needs to be done before the analysis"""

    @abstractmethod
    def analyse_datapoint(
        self,
        data_key: str,
        data_predicted,
        data_loaded,
        additional_data: dict,
        **kwargs,
    ) -> Optional[Any]:
        """Abstract method to analyze one datapoint"""

    @abstractmethod
    def get_final_metric(self) -> Optional[dict]:
        """This method is executed after all datapoints are processed"""
