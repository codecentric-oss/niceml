"""Module of the MultiPredictionHandler"""

from typing import List

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datainfos.datainfo import DataInfo
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.mlcomponents.predictionhandlers.predictionhandler import PredictionHandler


class CombinationPredictionHandler(PredictionHandler):
    """Prediction Handler that combines a list of `PredictionHandler`s"""

    def __init__(self, handlers: List[PredictionHandler]):
        super().__init__()
        self.handler_list: List[PredictionHandler] = handlers

    def set_params(
        self,
        exp_context: ExperimentContext,
        filename: str,
        data_description: DataDescription,
    ):
        for handler in self.handler_list:
            handler.set_params(exp_context, filename, data_description)
            handler.initialize()

    def __enter__(self):
        for handler in self.handler_list:
            handler.__enter__()

        return self

    def add_prediction(self, data_info_list: List[DataInfo], prediction_batch):
        for handler in self.handler_list:
            handler.add_prediction(data_info_list, prediction_batch)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        for handler in self.handler_list:
            handler.__exit__(exc_type, exc_value, exc_traceback)
