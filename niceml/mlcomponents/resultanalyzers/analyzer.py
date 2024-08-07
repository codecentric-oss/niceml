"""Module for the ABC ResultAnalyzer"""

from abc import ABC, abstractmethod

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext


class ResultAnalyzer(ABC):
    """After the prediction is done all data can be analyzed with a specific
    implementation of the ResultAnalyzer"""

    def __init__(self):
        """Initialize an abstract result analyzer."""

        self.data_description = None

    def initialize(self, *args, data_description: DataDescription, **kwargs):
        """Initializes the ResultAnalyzer and adds the data description. This isn't done by the
        `__init__` because some data is only available after initialising the ResultAnalyser, like
        data_description.

        Args:
            *args: Additional arguments that can be added to the ResultAnalyzer
            data_description:   DataDescription that is used by the ResultAnalyzer (available in the
                                `__call__` method). The data_description parameter contains
                                information about the data set, such as number of classes and
                                feature names.
            **kwargs: Additional keyword arguments that can be added to the ResultAnalyzer
        """
        self.data_description = data_description

    @abstractmethod
    def __call__(
        self, dataset: Dataset, exp_context: ExperimentContext, dataset_name: str
    ):
        """Method to analyze one dataset"""
