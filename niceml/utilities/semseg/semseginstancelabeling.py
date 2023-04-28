"""Module for SemSegInstanceLabel"""

from typing import Optional

import cv2
import numpy as np
from attr import define

from niceml.utilities.instancelabeling import InstanceLabel


@define
class SemSegInstanceLabel(InstanceLabel):  # pylint: disable = too-few-public-methods

    """`InstanceLabel` for one SemSeg error mask instance (prediction or ground truth)."""

    mask: Optional[np.ndarray] = None

    def calc_iou(self, other: "SemSegInstanceLabel") -> float:
        """
        Calculates the IOU of the masks of two `SemSegInstanceLabel`s

        Args:
            other: Second SemSegInstanceLabel to calculate the IOU with

        Returns:
            Calculated IOU
        """

        intersection = np.logical_and(self.mask, other.mask)
        union = np.logical_or(self.mask, other.mask)

        return np.sum(intersection) / np.sum(union)

    def scale_label(self, scale_factor: float) -> "SemSegInstanceLabel":
        """
        Scales an SemSegInstanceLabel by a given `scale_factor`

        Args:
            scale_factor: Factor to scale the SemSegInstanceLabel by

        Returns:
            Scaled instance of this SemSegInstanceLabel
        """
        scaled_mask = cv2.resize(  # pylint: disable = no-member
            self.mask,
            dsize=None,
            fx=scale_factor,
            fy=scale_factor,
            interpolation=cv2.INTER_NEAREST,  # pylint: disable = no-member,
        )
        return SemSegInstanceLabel(
            class_name=self.class_name,
            class_index=self.class_index,
            color=self.color,
            active=self.active,
            mask=scaled_mask,
        )
