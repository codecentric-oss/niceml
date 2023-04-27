"""Module for MaskVisualizer"""

from typing import List

import numpy as np
from PIL import Image

from niceml.dashboard.visualizers.imagevisualizer import ImageContainer, ImageVisualizer
from niceml.utilities.instancelabelmatching import get_kind_of_label_match
from niceml.utilities.semseg.semsegdrawing import draw_labels_on_image


class MaskVisualizer(
    ImageVisualizer
):  # pylint: disable = duplicate-code, too-few-public-methods
    """Visualizer for images with `SemSegInstanceLabel`s (prediction, ground truth)"""

    def __init__(
        self,
        hide_gt: bool = False,
        hide_gt_over_threshold: bool = True,
        iou_threshold: float = 0.5,
        match_gt_pred: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.match_gt_pred = match_gt_pred
        self.hide_gt = hide_gt
        self.hide_gt_over_threshold = hide_gt_over_threshold
        self.iou_threshold = iou_threshold

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

        if self.match_gt_pred:
            (
                image_data_container.predictions,
                image_data_container.ground_truth,
            ) = get_kind_of_label_match(
                pred_label_list=image_data_container.predictions,
                gt_label_list=image_data_container.ground_truth,
                hide_gt_over_thresh=self.hide_gt_over_threshold,
                iou_threshold=self.iou_threshold,
            )

        images = []
        for image_path in image_data_container.get_image_paths():
            try:
                images.append(
                    self.image_loader(
                        image_path, image_data_container.image_visu_size
                    ).astype(np.uint8)
                )
            except FileNotFoundError:
                image = Image.new(
                    mode="L",
                    size=image_data_container.image_visu_size.to_pil_size(),
                )
                image = np.array(image, dtype=np.uint8)
                images.append(image)

        images = [Image.fromarray(image).convert("RGB") for image in images]

        scale_factor = image_data_container.image_visu_size.get_division_factor(
            image_data_container.model_output_size
        )

        image_data_container = image_data_container.scale_instance_labels(
            scale_factor=scale_factor
        )

        draw_images = []

        for image in images:
            draw_image = draw_labels_on_image(
                image=image,
                pred_error_mask_label_list=image_data_container.predictions,
                gt_error_mask_label_list=image_data_container.ground_truth,
                hide_gt=self.hide_gt,
            )
            draw_images.append(draw_image)

        return [np.array(draw_image) for draw_image in draw_images]
