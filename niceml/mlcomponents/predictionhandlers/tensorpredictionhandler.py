"""Module for TensorPredictionHandler"""
import logging
from os.path import join
from typing import List

import numpy as np
import zarr
from numcodecs import GZip

from niceml.data.datainfos.datainfo import DataInfo
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.mlcomponents.predictionhandlers.predictionhandler import PredictionHandler
from niceml.utilities.fsspec.locationutils import open_location


class TensorPredictionHandler(PredictionHandler):
    """Gets tensors and stores them numpy compressed files"""

    def __init__(
        self,
        immediately_write: bool = False,
        round_decimals: int = None,
    ):
        super().__init__()
        self.immediately_write = immediately_write
        self.should_round = round_decimals is not None
        self.round_decimals = round_decimals
        self.data = None

    def __enter__(self):
        if not self.immediately_write:
            self.data = {}
        return self

    def add_prediction(self, data_info_list: List[DataInfo], prediction_batch):
        """adds a prediction after processed by the net"""
        if self.should_round:
            prediction_batch = np.round(prediction_batch, self.round_decimals)
        for idx, data_info in enumerate(data_info_list):
            cur_pred = prediction_batch[idx, :]
            if self.immediately_write:
                with open_location(self.exp_context.fs) as (exp_fs, exp_path):
                    with exp_fs.open(
                        join(
                            exp_path,
                            ExperimentFilenames.PREDICTION_FOLDER,
                            self.filename + ".npy",
                        ),
                        "wb",
                    ) as file:
                        np.save(
                            file,
                            cur_pred,
                        )
            else:
                self.data[data_info.get_identifier()] = cur_pred

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.immediately_write:
            return
        if self.data is None or len(self.data) == 0:
            # pylint: disable=logging-fstring-interpolation
            logging.getLogger(__name__).warning(
                f"PredictionHandler with image_filepath: "
                f"{self.filename} has no data to write!"
            )
        else:
            with open_location(self.exp_context.fs) as (exp_fs, exp_path):
                with exp_fs.open(
                    join(
                        exp_path,
                        ExperimentFilenames.PREDICTION_FOLDER,
                        self.filename + ".npz",
                    ),
                    "wb",
                ) as file:

                    np.savez_compressed(file, **self.data)


class TensorPredictionHandlerZarr(TensorPredictionHandler):
    """
    Saves tensors in da compressed Zarr directory.
    Each tensor is compressed with gzip.

    Parameters
    ----------
    key_seperator: str default ""
        string which seperates image_location and output type
    scale_to_int: bool, default False
        If true data is multiplied by 255
    save_as_int: bool, default False
        If true dtype of data is converted to uint8 to save space
    """

    def __init__(
        self,
        key_seperator: str = "",
        scale_to_int: bool = False,
        save_as_int: bool = False,
    ):
        super().__init__()
        self.save_as_int = save_as_int
        self.scale_to_int = scale_to_int
        self.key_seperator = key_seperator
        self.data = None

    def __enter__(self):
        self.data = zarr.open(join(self.filepath, self.filename + ".zarr"), mode="w")
        return self

    def add_prediction(self, data_info_list: List[DataInfo], prediction_batch):
        """adds a prediction after processed by the net"""
        if isinstance(prediction_batch, list):
            pred_list = zip(prediction_batch, self.data_description.get_output_names())
        else:
            pred_list = [(prediction_batch, "")]

        for prediction, suffix in pred_list:
            if self.scale_to_int:
                prediction = prediction * 255
            if self.save_as_int:
                prediction = prediction.astype(np.uint8)
            for idx, data_info in enumerate(data_info_list):
                cur_pred: np.ndarray = prediction[idx, :]
                # self.data[data_info.file_id] = cur_instance
                dataset = self.data.create(
                    data_info.get_identifier() + self.key_seperator + suffix,
                    shape=cur_pred.shape,
                    dtype=cur_pred.dtype,
                    compressor=GZip(level=7),
                    chunks=False,
                )
                dataset[:] = cur_pred

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass
