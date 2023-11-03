"""Module of the SemSegNetDataLogger"""
from typing import List, Tuple

import numpy as np
from PIL import Image

from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputImageDataDescription,
)
from niceml.data.datainfos.imagedatainfo import ImageDataInfo
from niceml.data.datainfos.semsegdatainfo import SemSegDataInfo
from niceml.data.netdataloggers.netdatalogger import NetDataLogger
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.utilities.colorutils import get_color_array
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.semseg.semsegdrawing import draw_error_mask_on_image
from niceml.utilities.semseg.semseginstancelabeling import SemSegInstanceLabel


class SemSegNetDataLogger(NetDataLogger):
    """NetDataLogger for semantic segmentation"""

    def __init__(self, max_log: int = 10, scale: bool = True):
        """initialize SemSegNetDataLogger parameters"""
        super().__init__()
        self.scale: bool = scale  # If true, the masks are scaled to the image size.
        # If false the images are scaled to the mask size.
        self.max_log: int = max_log
        self.log_count: int = 0
        self.mask_colors: List[Tuple[int]] = []

    def initialize(
        self,
        data_description: OutputImageDataDescription,
        exp_context: ExperimentContext,
        set_name: str,
    ):
        """initialize SemSegNetDataLogger parameters before training"""
        super().initialize(
            data_description=data_description,
            exp_context=exp_context,
            set_name=set_name,
        )

        mask_colors = get_color_array(
            list(range(self.data_description.get_output_channel_count()))
        )
        self.mask_colors = [
            [int(value * 255) for value in color] for color in mask_colors
        ]

    # pylint: disable=too-many-locals
    def log_data(
        self,
        net_inputs: np.ndarray,
        net_targets: np.ndarray,
        data_info_list: List[SemSegDataInfo],
    ):
        """
        Saves as many images with corresponding masks as defined in `self.max_log`.
        The images are saved into `self.output_path`. For each input image,
        the associated masks are added to the image.

        Args:
            net_inputs: Input images as `np.ndarray`
            net_targets: Target masks as `np.ndarray` scaled by OUTPUT_IMAGE_SIZE_DIVISOR
            data_info_list: Associated data information of input and
            destination with extended information

        Returns:
            None
        """
        if self.log_count >= self.max_log:
            return

        for net_input, net_target, data_info in zip(
            net_inputs, net_targets, data_info_list
        ):
            instance_labels = [
                SemSegInstanceLabel(
                    class_name=self.data_description.get_output_channel_names()[
                        class_idx
                    ],
                    class_index=class_idx,
                    color=tuple(self.mask_colors[class_idx]),
                    active=True,
                    mask=net_target[:, :, class_idx] * 255,
                    # `draw_error_mask_on_image` doesn't work with binary masks.
                    # RGB values are required. * 255 converts mask to RGB
                )
                for class_idx in range(self.data_description.get_output_channel_count())
                if net_target[:, :, class_idx].max() > 0
            ]

            if self.scale:
                factor = ImageSize(
                    net_input.shape[1], net_input.shape[0]
                ).get_division_factor(self.data_description.get_output_image_size())
                instance_labels = [
                    label.scale_label(scale_factor=factor) for label in instance_labels
                ]

            self._draw_image(
                image=net_input,
                instance_labels=instance_labels,
                data_info=data_info,
            )
            self.log_count += 1
            if self.log_count >= self.max_log:
                break

    def _draw_image(
        self,
        image: np.ndarray,
        instance_labels: List[SemSegInstanceLabel],
        data_info: ImageDataInfo,
    ):
        """
        Draws image including its associated instance labels and saves it.
        Args:
            image: image that will be saved
            instance_labels: Instance labels to draw on the image.
            data_info: Data Info to get the filename from

        Returns:
            None
        """
        img = Image.fromarray(image).convert("RGB")
        if not self.scale:
            img = img.resize(
                size=self.data_description.get_output_image_size().to_pil_size()
            )

        for label in instance_labels:
            img = draw_error_mask_on_image(label=label, image=img)

        self._save_img(
            image=img,
            filename=f"{data_info.get_filename()}.png",
        )
