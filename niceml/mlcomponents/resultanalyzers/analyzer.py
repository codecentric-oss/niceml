"""Module for the ABC ResultAnalyzer"""
from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel, Field

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext


class ResultAnalyzer(ABC):
    """After the prediction is done all data can be analyzed with a specific
    implementation of the ResultAnalyzer"""

    def __init__(self, data_description: Optional[DataDescription] = None):
        self.data_description = data_description

    def initialize(self, data_description: DataDescription):
        """Initializes the resultanalyzer and adds the data description"""
        self.data_description = data_description

    @abstractmethod
    def __call__(
        self, dataset: Dataset, exp_context: ExperimentContext, dataset_name: str
    ):
        """Method to analyze one dataset"""
