"""Module for semseg prediction handlers"""
import logging
from os.path import join
from typing import List, Tuple

import cv2
import numpy as np
import pandas as pd
from PIL import Image

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datadescriptions.outputdatadescriptions import OutputImageDataDescription
from niceml.data.datainfos.datainfo import DataInfo
from niceml.data.dataiterators.boundingboxdataiterator import DETECTION_INDEX_COLUMN_NAME
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.mlcomponents.predictionhandlers.predictionhandler import PredictionHandler
from niceml.mlcomponents.resultanalyzers.instancefinders.instancefinder import (
    InstanceFinder,
)
from niceml.mlcomponents.resultanalyzers.instancefinders.maskinstance import MaskInstance
from niceml.mlcomponents.resultanalyzers.tensors.semsegdataiterator import (
    SemSegPredictionContainer,
)
from niceml.utilities.boundingboxes.boundingbox import get_bounding_box_attributes


class SemSegMaskPredictionHandler(PredictionHandler):
    """Prediction handler to convert a tensor to channel images for SemSeg"""

    def __init__(self, img_extension: str = ".png", prediction_suffix: str = "_pred"):
        """
        This prediction handler converts a tensor to the maximum prediction image

        Parameters
        ----------
        img_extension: str
            Type of the images to write.
        """
        super().__init__()
        self.img_extension = img_extension
        self.prediction_suffix = prediction_suffix

    def __enter__(self):
        return self

    def add_prediction(self, data_info_list: List[DataInfo], prediction_batch):
        """After each prediction this is processed to store the images."""

        for prediction, data_info in zip(prediction_batch, data_info_list):
            values = np.max(prediction, axis=2) * 255
            value_idxes = np.argmax(prediction, axis=2)
            target_array = np.stack(
                (values, value_idxes, np.zeros_like(values)), axis=2
            ).astype(dtype=np.uint8)
            target_image = Image.fromarray(target_array)
            self.exp_context.write_image(
                target_image,
                join(
                    ExperimentFilenames.PREDICTION_FOLDER,
                    self.filename,
                    f"{data_info.get_identifier()}{self.prediction_suffix}{self.img_extension}",
                ),
            )

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass


class SemSegBBoxPredictionHandler(PredictionHandler):
    """Prediction handler to convert a tensor to bounding box information corresponding
    to `ObjDetPredictionHandler` based on found  instances in a prediction mask."""

    def __init__(
        self,
        instance_finder: InstanceFinder,
        prediction_prefix: str = "pred",
        pred_identifier: str = "image_filepath",
        detection_idx_col: str = DETECTION_INDEX_COLUMN_NAME,
    ):
        super().__init__()
        self.prediction_prefix = prediction_prefix
        self.instance_finder = instance_finder
        self.pred_identifier = pred_identifier
        self.detection_idx_col = detection_idx_col
        self.data = None
        self.data_columns = [pred_identifier, detection_idx_col]
        self.data_columns += get_bounding_box_attributes()

    def set_params(
        self,
        exp_context: ExperimentContext,
        filename: str,
        data_description: DataDescription,
    ):
        super().set_params(exp_context, filename, data_description)
        self.instance_finder.initialize(
            data_description=data_description,
            exp_context=exp_context,
            dataset_name=filename,
        )

    def __enter__(self):
        self.data = []
        if isinstance(self.data_description, OutputImageDataDescription):
            for class_count in range(self.data_description.get_output_channel_count()):
                self.data_columns.append(f"{self.prediction_prefix}_{class_count:04d}")
        return self

    def _add_data(
        self,
        identifier: str,
        predictions: List[float],
        detection_index: int,
    ):
        """Adds a prediction entry to `self.data`"""

        col_list: list = [identifier, detection_index] + predictions
        self.data.append(dict(zip(self.data_columns, col_list)))

    # pylint: disable = too-many-locals
    def add_prediction(self, data_info_list: List[DataInfo], prediction_batch):
        """After each prediction, this is processed to find  instances in a mask
        and create bounding box coordinates from the found instances"""

        if (
            len(prediction_batch.shape) < 4
        ):  # If the batch size is 1 a additional dimension is necessary and added below
            prediction_batch = np.expand_dims(prediction_batch, 0)
        for prediction, data_info in zip(prediction_batch, data_info_list):
            values = np.max(prediction, axis=2)

            value_idxes = np.argmax(prediction, axis=2)

            prediction_container = SemSegPredictionContainer(
                image_id=None,
                max_prediction_idxes=value_idxes,
                max_prediction_values=values,
            )

            mask_instances: List[MaskInstance] = self.instance_finder.analyse_datapoint(
                data_key="",
                data_predicted=prediction_container,
                data_loaded=None,
                additional_data={},
            )

            bbox_pred_data = create_bbox_prediction_from_mask_instances(
                prediction=prediction,
                mask_instances=mask_instances,
            )
            for detection_idx, predictions in bbox_pred_data:
                self._add_data(
                    identifier=data_info.get_identifier(),
                    predictions=predictions,
                    detection_index=detection_idx,
                )

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Save the data in `self.data` as a parquet file"""
        if self.data is None:
            logging.getLogger(__name__).warning(
                "PredictionHandler: %s has no data to write!",
                self.filename,
            )
        else:
            data_frame: pd.DataFrame = pd.DataFrame(self.data)
            self.exp_context.write_parquet(
                data_frame,
                join(ExperimentFilenames.PREDICTION_FOLDER, self.filename + ".parq"),
            )


def create_bbox_prediction_from_mask_instances(
    prediction: np.ndarray,
    mask_instances: List[MaskInstance],
) -> List[Tuple[int, List[float]]]:
    """
    Creates a prepared list of bounding box prediction information
    based on the result of a semantic segmentation
    Args:
        prediction: raw prediction data with the shape
                    (image_width, image_height, channel_count)
        mask_instances: found instances of a mask

    Returns:
        List of Tuples (detection_index, list of prediction data
        (bbox coordinates and prediction scores of each output channel))

    """
    detection_idx_count: int = 0
    bbox_prediction_data: List[Tuple[int, List[float]]] = []

    if (
        len(mask_instances) == 0
        and sum(len(error_info.instance_contours) for error_info in mask_instances) == 0
    ):
        bbox_prediction_data.append(
            (-1, [0.0 for _ in range(4 + prediction.shape[-1])])
        )

    for error_info in mask_instances:
        # pylint: disable = no-member
        for error in error_info.instance_contours:

            poly = cv2.approxPolyDP(error.contour, epsilon=1, closed=True)
            # epsilon is the approximation accuracy
            # (max difference between the original and the approximation)

            x_pos, y_pos, width, height = cv2.boundingRect(poly)
            predictions_of_error = prediction[
                y_pos : y_pos + height, x_pos : x_pos + width, :
            ]
            bbox_prediction_data.append(
                (
                    detection_idx_count,
                    [float(coord) for coord in [x_pos, y_pos, width, height]]
                    + list(np.max(predictions_of_error, axis=(0, 1))),
                )
            )
            detection_idx_count += 1
    return bbox_prediction_data
