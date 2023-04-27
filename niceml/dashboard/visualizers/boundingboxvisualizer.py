"""Module for BoundingBoxVisualizer"""
import logging
from typing import List

import numpy as np
from PIL import Image

from niceml.dashboard.visualizers.imagevisualizer import (
    ImageContainer,
    ImageVisualizer,
    check_instance_label_type,
)
from niceml.utilities.boundingboxes.bboxdrawing import draw_labels_on_image
from niceml.utilities.boundingboxes.bboxlabeling import ObjDetInstanceLabel


class BoundingBoxVisualizer(ImageVisualizer):  # pylint: disable=too-few-public-methods
    """Visualizer for images with ObjDetInstanceLabels (prediction and ground truth)"""

    def __init__(
        self,
        hide_gt: bool = False,
        hide_gt_over_threshold: bool = True,
        iou_threshold: float = 0.5,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.iou_threshold = iou_threshold
        self.hide_gt = hide_gt
        self.hide_gt_over_threshold = hide_gt_over_threshold

    def get_images_with_labels(
        self, image_data_container: ImageContainer
    ) -> List[np.ndarray]:
        """
        Returns images of 'image_data_container' with drawn prediction and ground truth labels

        Args:
            image_data_container: Container with an images label information

        Returns:
            List of images with prediction and ground truth labels drawn on them
        """
        images = []
        for image_path in image_data_container.get_image_paths():
            try:
                image = self.image_loader(image_path).astype(np.uint8)
                images.append(image)
            except FileNotFoundError:
                logging.getLogger(__name__).warning("FileNotFoundError: %s", image_path)
        images = [
            Image.fromarray(image)
            .convert("RGB")
            .resize(size=image_data_container.image_visu_size.to_pil_size())
            for image in images
        ]

        draw_images = []

        if not check_instance_label_type(
            label_list=image_data_container.predictions, target_type=ObjDetInstanceLabel
        ) and not check_instance_label_type(
            label_list=image_data_container.ground_truth,
            target_type=ObjDetInstanceLabel,
        ):
            raise ValueError(
                "Type of predictions and ground truth labels is not ObjDetInstanceLabel"
            )
        scale_factor = image_data_container.image_visu_size.get_division_factor(
            image_data_container.model_output_size
        )
        image_data_container = image_data_container.scale_instance_labels(
            scale_factor=scale_factor
        )

        for image in images:
            draw_image = draw_labels_on_image(
                image=image,
                pred_bbox_label_list=image_data_container.predictions,
                gt_bbox_label_list=image_data_container.ground_truth,
                hide_gt=self.hide_gt,
                hide_gt_over_thresh=self.hide_gt_over_threshold,
                iou_threshold=self.iou_threshold,
            )
            draw_images.append(draw_image)

        return [np.array(draw_image) for draw_image in draw_images]
