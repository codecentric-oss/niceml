"""Module for anchor encoding"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from niceml.utilities.boundingboxes.bboxconversion import compute_target_gt_array
from niceml.utilities.boundingboxes.bboxencoding import decode_boxes
from niceml.utilities.boundingboxes.bboxlabeling import ObjDetInstanceLabel
from niceml.utilities.boundingboxes.boundingbox import (
    IGNORE_MASK_VALUE,
    NEGATIVE_MASK_VALUE,
    POSITIVE_MASK_VALUE,
    BoundingBox,
)
from niceml.utilities.ioumatrix import compute_iou_matrix


class AnchorEncoder(ABC):  # pylint: disable=too-few-public-methods
    """Abstract AnchorEncoder"""

    @abstractmethod
    def encode_anchors(
        self,
        anchor_list: List[BoundingBox],
        gt_labels: List[ObjDetInstanceLabel],
        num_classes: int,
        box_variance: List[float],
    ) -> np.ndarray:
        """Encodes an anchor list with corresponding labels to a numpy array"""

    @abstractmethod
    def decode_anchors(self, anchor_list: List[BoundingBox], encodings: np.ndarray):
        """ "Decodes an anchor list with corresponding labels to a numpy array"""


@dataclass
class SimpleAnchorEncoder(AnchorEncoder):
    """Class to encode anchors before model optimization"""

    match_iou: float = 0.5
    ignore_iou: float = 0.4

    def encode_anchors(  # pylint: disable=too-many-locals
        self,
        anchor_list: List[BoundingBox],
        gt_labels: List[ObjDetInstanceLabel],
        num_classes: int,
        box_variance: List[float],
    ) -> np.ndarray:
        """Encodes an anchor list to a numpy array"""
        encoded_feature_list: List[List[float]] = []

        for anchor in anchor_list:

            if len(gt_labels) == 0:
                target_bbox = anchor
                target_label = None
                prediction_flag = NEGATIVE_MASK_VALUE
            else:

                max_iou = 0
                target_bbox = gt_labels[0].bounding_box
                target_label = None
                prediction_flag = NEGATIVE_MASK_VALUE

                for label_instance in gt_labels:
                    gt_bbox = label_instance.bounding_box
                    iou = anchor.calc_iou(gt_bbox)

                    if iou > max_iou:
                        max_iou = iou
                        target_bbox = gt_bbox
                        target_label = label_instance.class_index
                        prediction_flag = POSITIVE_MASK_VALUE

                if self.match_iou > max_iou > self.ignore_iou:
                    target_label = None
                    prediction_flag = IGNORE_MASK_VALUE

                elif max_iou < self.ignore_iou:
                    target_label = None
                    prediction_flag = NEGATIVE_MASK_VALUE

            cur_encoding = anchor.encode(target_bbox, box_variance)
            cur_encoding.append(prediction_flag)
            target_label_vector = [0] * num_classes
            if target_label is not None:
                target_label_vector[target_label] = 1
            cur_encoding += target_label_vector
            encoded_feature_list.append(cur_encoding)

        target_bbox_array = np.array(encoded_feature_list)
        return target_bbox_array

    def decode_anchors(
        self, anchor_list: List[BoundingBox], encodings: np.ndarray
    ) -> np.ndarray:
        """
        Decodes encoded bounding boxes
        Args:
            anchor_list: List of bounding boxes representing the anchors
            encodings: 2D array with at least the four coordinates
            of the bounding boxes in xywh format.
            This is optionally followed by a mask flag (POSITIVE,NEGATIVE,IGNORE)
            and a one-hot encoded class vector

        Returns:
            Same as encodings but with decoded bounding box coordinates

        """
        decoded_box_predictions: List[np.ndarray] = []

        for anchor, prediction in zip(anchor_list, encodings):
            box_variance = self.box_variance  # pylint: disable=no-member
            decoded_box = anchor.decode(
                predicted_values=list(prediction[:4]), box_variance=box_variance
            )

            decoded_box_predictions.append(
                np.array(list(decoded_box.get_absolute_ullr()))
            )
        decoded_box_prediction_array = np.array(decoded_box_predictions)
        encodings[:, :4] = decoded_box_prediction_array

        return encodings


@dataclass
class OptimizedAnchorEncoder(AnchorEncoder):
    """Class to encode anchors before model optimization"""

    match_iou: float = 0.5
    ignore_iou: float = 0.4
    anchor_array_stored_ullr: Optional[np.ndarray] = None
    anchor_array_stored_xywh: Optional[np.ndarray] = None

    def encode_anchors(
        self,
        anchor_list: List[BoundingBox],
        gt_labels: List[ObjDetInstanceLabel],
        num_classes: int,
        box_variance: List[float],
    ) -> np.ndarray:
        """Encodes an anchor list to a numpy array"""
        box: BoundingBox
        label: ObjDetInstanceLabel
        if (
            self.anchor_array_stored_ullr is None
            or len(anchor_list) != self.anchor_array_stored_ullr.shape[0]
        ):
            self.anchor_array_stored_ullr = np.array(
                [box.get_absolute_ullr() for box in anchor_list]
            )

        if len(gt_labels) == 0:
            anchor_shape = self.anchor_array_stored_ullr.shape
            target_array = np.zeros(
                (anchor_shape[0], anchor_shape[1] + 1 + num_classes)
            )
            target_array[:, anchor_shape[1]] = NEGATIVE_MASK_VALUE
            return target_array

        gt_box_array = np.array(
            [label.bounding_box.get_absolute_ullr() for label in gt_labels]
        )
        iou_matrix = compute_iou_matrix(self.anchor_array_stored_ullr, gt_box_array)
        class_index_array = np.array([label.class_index for label in gt_labels])
        target_array = compute_target_gt_array(
            self.anchor_array_stored_ullr,
            gt_box_array,
            iou_matrix=iou_matrix,
            box_variances=np.array(box_variance),
            class_index_array=class_index_array,
            match_iou=self.match_iou,
            ignore_iou=self.ignore_iou,
            num_classes=num_classes,
        )
        return target_array

    def decode_anchors(self, anchor_list: List[BoundingBox], encodings: np.ndarray):
        """
        Decodes encoded bounding boxes in an optimized way
        Args:
            anchor_list: List of bounding boxes representing the anchors
            encodings: 2D array with at least the four coordinates
            of the bounding boxes in xywh format.
            This is optionally followed by a mask flag (POSITIVE,NEGATIVE,IGNORE)
            and a one-hot encoded class vector

        Returns:
            Same as encodings but with decoded bounding box coordinates

        """

        if (
            self.anchor_array_stored_xywh is None
            or len(anchor_list) != self.anchor_array_stored_xywh.shape[0]
        ):
            self.anchor_array_stored_xywh = np.array(
                [box.get_absolute_ullr() for box in anchor_list]
            )

        box_variance = self.box_variance  # pylint: disable=no-member
        decoded_boxes = decode_boxes(
            anchor_boxes_xywh=self.anchor_array_stored_xywh,
            encoded_array_xywh=encodings[:, :4],
            box_variances=np.array(box_variance),
        )

        encodings[:, :4] = decoded_boxes

        return encodings
