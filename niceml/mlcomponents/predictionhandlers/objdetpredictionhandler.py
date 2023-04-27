"""Module with a prediction handler for object detection and also supportive functions """

import logging
from os.path import join
from typing import List

import numpy as np
import pandas as pd
from attrs import asdict

from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputObjDetDataDescription,
)
from niceml.data.datainfos.objdetdatainfo import ObjDetDataInfo
from niceml.data.dataiterators.boundingboxdataiterator import (
    DETECTION_INDEX_COLUMN_NAME,
    NO_PREDICTIONS_DETECTION_VALUE,
)
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.mlcomponents.objdet.anchorgenerator import AnchorGenerator
from niceml.mlcomponents.predictionhandlers.predictionhandler import PredictionHandler
from niceml.utilities.boundingboxes.bboxencoding import decode_boxes
from niceml.utilities.boundingboxes.boundingbox import BoundingBox
from niceml.utilities.boundingboxes.filtering.predictionfilter import PredictionFilter
from niceml.utilities.commonutils import check_instance


# pylint:disable=too-many-arguments,too-many-instance-attributes)
class ObjDetPredictionHandler(PredictionHandler):
    """Prediction handler for object detection predictions (BoundingBox, class prediction)"""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        prediction_filter: PredictionFilter,
        prediction_prefix: str = "pred",
        pred_identifier: str = "image_location",
        detection_idx_col: str = DETECTION_INDEX_COLUMN_NAME,
        apply_sigmoid: bool = True,
    ):

        super().__init__()
        self.prediction_filter = prediction_filter
        self.prediction_prefix = prediction_prefix
        self.apply_sigmoid = apply_sigmoid
        self.pred_identifier = pred_identifier
        self.detection_idx_col = detection_idx_col
        self.data = None
        self.data_columns = [pred_identifier, detection_idx_col]
        self.data_columns += list(asdict(BoundingBox(0, 0, 0, 0)).keys())

        self.anchor_generator = AnchorGenerator()
        self.anchors = None
        self.anchor_array = None

    def initialize(self):
        self.anchors: List[BoundingBox] = self.anchor_generator.generate_anchors(
            data_description=self.data_description
        )
        self.anchor_array = np.array([box.get_absolute_xywh() for box in self.anchors])
        self.prediction_filter.initialize(data_description=self.data_description)

    def __enter__(self):
        """Init `self.data` after the context is entered"""
        self.data = []
        if isinstance(self.data_description, OutputObjDetDataDescription):
            for class_count in range(self.data_description.get_output_class_count()):
                self.data_columns.append(f"{self.prediction_prefix}_{class_count:04d}")
        return self

    def _add_data(
        self,
        identifier: str,
        prediction: np.ndarray,
        detection_index: int,
    ):
        """Adds a prediction entry to `self.data` including to final predictions"""
        prediction_list: List[float] = [float(pred) for pred in prediction]
        col_list: list = [identifier, detection_index] + prediction_list
        self.data.append(dict(zip(self.data_columns, col_list)))

    def _decode_box_predictions(self, box_predictions) -> np.ndarray:
        """Decode the predictions into real bounding box coordinates"""

        decoded_boxes = decode_boxes(
            anchor_boxes_xywh=self.anchor_array,
            encoded_array_xywh=box_predictions[:, :4],
            box_variances=np.array(self.data_description.get_box_variance()),
        )

        box_predictions[:, :4] = decoded_boxes
        return box_predictions

    def add_prediction(
        self, data_info_list: List[ObjDetDataInfo], prediction_batch: np.ndarray
    ):
        """Gets the results of an object detection model, de"""
        output_dd: OutputObjDetDataDescription = check_instance(
            self.data_description, OutputObjDetDataDescription
        )
        for curr_batch, curr_data_info in zip(prediction_batch, data_info_list):
            decoded_box_predictions = self._decode_box_predictions(
                box_predictions=curr_batch
            )

            if self.apply_sigmoid:
                decoded_box_predictions = apply_sigmoid_on_cls_predictions(
                    decoded_box_predictions,
                    output_dd.get_coordinates_count(),
                )

            filtered_box_predictions = self.prediction_filter.filter(
                decoded_box_predictions
            )

            if len(filtered_box_predictions) > 0:
                for curr_index, prediction in enumerate(filtered_box_predictions):
                    self._add_data(
                        identifier=curr_data_info.get_identifier(),
                        prediction=prediction,
                        detection_index=curr_index,
                    )
            else:
                prediction = np.zeros(
                    (
                        output_dd.get_coordinates_count()
                        + output_dd.get_output_class_count(),
                    )
                )
                self._add_data(
                    curr_data_info.get_identifier(),
                    prediction=prediction,
                    detection_index=NO_PREDICTIONS_DETECTION_VALUE,
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


def apply_sigmoid_on_cls_predictions(
    box_predictions: np.ndarray, coordinates_count: int
) -> np.ndarray:
    """Applies sigmoid only on the classification part"""
    box_predictions[:, coordinates_count:] = 1 / (
        1 + np.exp(-box_predictions[:, coordinates_count:])
    )
    return box_predictions
