"""Module for MultiResultAnalyzer"""
from typing import List

from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.mlcomponents.resultanalyzers.analyzer import ResultAnalyzer


class MultiResultAnalyzer(ResultAnalyzer):
    """contains multiple ResultAnalyzer which are called consequently"""

    def __init__(self, analyzers: List[ResultAnalyzer]):
        super().__init__()
        self.analyzers: List[ResultAnalyzer] = analyzers

    def __call__(
        self, dataset: Dataset, exp_context: ExperimentContext, dataset_name: str
    ):
        for cur_analyzer in self.analyzers:
            cur_analyzer(dataset, exp_context, dataset_name)
