"""Module for the abstract PredictionHandler"""

from abc import ABC, abstractmethod
from typing import List

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datainfos.datainfo import DataInfo
from niceml.experiments.experimentcontext import ExperimentContext


class PredictionHandler(ABC):
    """Abstract PredictionHandler class to implement your own prediction handler"""

    def __init__(self):
        self.exp_context = None
        self.filename = None
        self.data_description = None

    def set_params(
        self,
        exp_context: ExperimentContext,
        filename: str,
        data_description: DataDescription,
    ):
        self.exp_context = exp_context
        self.filename = filename
        self.data_description = data_description

    def initialize(self, *args, **kwargs):
        """
        This method can be implemented if some initialization steps need
        values that are specified in set_params
        Returns:

        """

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def add_prediction(self, data_info_list: List[DataInfo], prediction_batch):
        """Consumes a prediction batch and handles the predicted data
        to create an experiment output"""

    @abstractmethod
    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass
