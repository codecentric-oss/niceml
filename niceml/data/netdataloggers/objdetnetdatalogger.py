"""Module of the ObjDetNetDataLogger"""

from os.path import join
from typing import List

import numpy as np
from PIL import Image

from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputObjDetDataDescription,
)
from niceml.data.datainfos.imagedatainfo import ImageDataInfo
from niceml.data.datainfos.objdetdatainfo import ObjDetDataInfo
from niceml.data.netdataloggers.netdatalogger import NetDataLogger
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.mlcomponents.objdet.anchorgenerator import AnchorGenerator
from niceml.utilities.boundingboxes.bboxdrawing import draw_bounding_box_on_image
from niceml.utilities.boundingboxes.bboxlabeling import ObjDetInstanceLabel
from niceml.utilities.boundingboxes.boundingbox import (
    POSITIVE_MASK_VALUE,
    bounding_box_from_ullr,
)
from niceml.utilities.colorutils import Color
from niceml.utilities.commonutils import check_instance


class ObjDetNetDataLogger(NetDataLogger):
    """NetDataLogger for object detection"""

    def __init__(self, max_log: int = 5):
        super().__init__()
        self.max_log: int = max_log
        self.anchor_generator: AnchorGenerator = AnchorGenerator()
        self.log_count: int = 0

    # pylint: disable=too-many-locals
    def log_data(
        self,
        net_inputs: np.ndarray,
        net_targets: np.ndarray,
        data_info_list: List[ObjDetDataInfo],
    ):
        """
        Saves as many images with corresponding anchor boxes as defined in `self.max_log`.
        The images are saved into `self.output_path`. For each input image,
        the associated positively marked anchor boxes are added to the image.

        Args:
            net_inputs: Input images as `np.ndarray`
            net_targets: Targets as `np.ndarray` with the coded coordinates
                of the anchor boxes, the mask value and the one-hot-encoded class vector
            data_info_list: Associated data information of input and destination
                with extended information

        Returns:
            None
        """
        if self.log_count >= self.max_log:
            return

        output_data_description = check_instance(
            self.data_description, OutputObjDetDataDescription
        )

        anchors = self.anchor_generator.generate_anchors(
            data_description=output_data_description
        )

        if len(net_inputs) != len(net_targets):
            raise ValueError(
                f"Mismatching lengths of net_inputs "
                f"and net_targets ({len(net_inputs)}, {len(net_targets)}"
            )

        for net_input, net_target, data_info in zip(
            net_inputs, net_targets, data_info_list
        ):
            decoded_bboxes = [
                anchor.decode(
                    predicted_values=target[:4],
                    box_variance=output_data_description.get_box_variance(),
                ).get_absolute_ullr()
                for anchor, target in zip(anchors, net_target)
            ]
            net_target[:, :4] = decoded_bboxes
            positive_targets = net_target[net_target[:, 4] == POSITIVE_MASK_VALUE]
            labels = [
                self._target_to_label(target=target) for target in positive_targets
            ]
            self._draw_image(
                image=net_input, instance_labels=labels, data_info=data_info
            )

            self.log_count += 1

            if self.log_count >= self.max_log:
                break

    def _draw_image(
        self,
        image: np.ndarray,
        instance_labels: List[ObjDetInstanceLabel],
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
        for label in instance_labels:
            img = draw_bounding_box_on_image(label=label, image=img)
        self._save_img(image=img, filename=data_info.get_filename())

    def _target_to_label(self, target: np.ndarray) -> ObjDetInstanceLabel:
        output_dd = check_instance(self.data_description, OutputObjDetDataDescription)

        bbox = bounding_box_from_ullr(*target[:4])
        class_idx = np.argmax(target[5:])
        class_name = output_dd.get_output_class_names()[class_idx]
        return ObjDetInstanceLabel(
            class_name=class_name,
            class_index=int(class_idx),
            bounding_box=bbox,
            color=Color.RED,
            active=True,
        )
