import logging
from collections import defaultdict
from os.path import join
from typing import List, Union

import numpy as np
import pandas as pd

from niceml.data.datainfos.datainfo import DataInfo
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.mlcomponents.predictionhandlers.predictionhandler import PredictionHandler


class VectorPredictionHandler(PredictionHandler):
    def __init__(
        self,
        use_output_names: bool = False,
        prediction_prefix: str = "pred",
    ):
        super().__init__()
        self.use_output_names = use_output_names
        self.prediction_prefix = prediction_prefix

    def __enter__(self):
        self.data = defaultdict(list)
        return self

    def _get_pred_name(self, cur_output_idx: int) -> str:
        if self.use_output_names:
            return self.data_description.get_output_names()[cur_output_idx] + "_pred"
        else:
            return self.prediction_prefix

    def _update_data(self, prediction: np.ndarray, cur_output_index: int = 0):
        pred_str: str = self._get_pred_name(cur_output_index)
        if len(prediction.shape) == 2:
            for col in range(prediction.shape[1]):
                pred_list = list(prediction[:, col])
                self.data[f"{pred_str}_{col:04d}"] += pred_list
        elif len(prediction.shape) == 1:
            self.data[f"{pred_str}_0000"] += list(prediction)
        else:
            raise Exception(
                f"Data with Dim > 2 not supported - Actual Dim: {prediction.shape}"
            )

    def add_prediction(
        self, data_info: List[DataInfo], prediction: Union[np.ndarray, list]
    ):
        for di in data_info:
            di_dict: dict = di.get_info_dict()
            for key, value in di_dict.items():
                self.data[key].append(value)
        if type(prediction) is list:
            for idx, cur_pred in enumerate(prediction):
                self._update_data(cur_pred, idx)
        else:
            self._update_data(prediction)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.data is None:
            logging.getLogger(__name__).warning(
                f"PredictionHandler with filename: "
                f"{self.filename} has no data to write!"
            )
        else:
            data_frame: pd.DataFrame = pd.DataFrame(self.data)
            self.exp_context.write_parquet(
                data_frame,
                join(ExperimentFilenames.PREDICTION_FOLDER, self.filename + ".parq"),
            )
