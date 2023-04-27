"""Module for data classes representing the found error instances in a predicted image"""
from dataclasses import dataclass
from typing import Optional, Tuple, Union

import cv2
import numpy as np

from niceml.utilities.imagesize import ImageSize


@dataclass
class InstanceContour:
    """Dataclass that represents a instance contour."""

    contour: np.ndarray
    class_idx: Optional[int] = None

    # pylint: disable = no-member
    def intersects_mask(self, mask: np.ndarray) -> bool:
        """
        Check if `self.contour` intersect with `mask`.

        Args:
            mask: mask to check for intersection

        Returns:
            True if there is an intersection

        """

        defect_mask = np.zeros_like(mask)
        cv2.drawContours(
            defect_mask, [self.contour], -1, color=(1,), thickness=cv2.FILLED
        )
        intersect = np.logical_and(mask, defect_mask)
        return np.any(intersect)

    # pylint: disable = no-member
    def get_contour_mask(
        self, target_shape: Union[ImageSize, Tuple[int, int]]
    ) -> np.ndarray:
        """
        Creates a Mask from `self.contour with `target_shape`
        Args:
            target_shape: Shape of the mask

        Returns:
            Mask with `self.contour` on it and the form `target_shape`.
        """

        target_shape = (
            target_shape.to_numpy_shape()
            if isinstance(target_shape, ImageSize)
            else target_shape
        )
        mask = np.zeros(shape=target_shape)
        mask = cv2.drawContours(
            mask,
            [self.contour],
            -1,
            color=(255,),
            thickness=cv2.FILLED,
        )
        return mask
