"""Module for ObjDetInstanceLabel"""
from typing import List, Optional, Union

from attr import define, field

from niceml.utilities.boundingboxes.bboxconversion import dict_to_bounding_box
from niceml.utilities.boundingboxes.boundingbox import BoundingBox, bounding_box_from_ullr
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.instancelabeling import InstanceLabel


@define
class ObjDetInstanceLabel(InstanceLabel):  # pylint: disable=too-few-public-methods
    """Label information for one specific bounding box and its prediction score"""

    bounding_box: Union[BoundingBox, None] = field(
        converter=dict_to_bounding_box, default=None
    )
    score: Optional[float] = None
    rotation: int = None

    def calc_iou(self, other: "ObjDetInstanceLabel") -> float:
        """
        Calculates the IOU of two given `ObjDetInstanceLabel`s bounding boxes

        Args:
            other: ObjDetInstanceLabel to calculate the IOU for

        Returns:
            Calculated IOU
        """
        return self.bounding_box.calc_iou(  # pylint: disable=no-member
            other=other.bounding_box
        )

    def to_content_list(self) -> list:
        """
        Creates a list with the contents of the ObjDetInstanceLabel in the following order:
        1. all bounding boxes (separately),
        2. class name,
        3. class index,
        4. prediction score,
        5. rotation
        """
        content_list = list(  # pylint: disable=no-member
            self.bounding_box.get_absolute_ullr()
        )
        content_list += [self.class_name, self.class_index, self.score, self.rotation]
        return content_list

    def scale_label(self, scale_factor: float) -> "ObjDetInstanceLabel":
        """
        Scales an ObjDetInstanceLabel by a given `scale_factor`

        Args:
            scale_factor: Factor to scale the ObjDetInstanceLabel by

        Returns:
            Scaled instance of this ObjDetInstanceLabel"""
        return ObjDetInstanceLabel(
            class_name=self.class_name,
            class_index=self.class_index,
            color=self.color,
            active=self.active,
            bounding_box=self.bounding_box.scale(scale_factor),
            score=self.score,
            rotation=self.rotation,
        )


def obj_instance_factory_from_content_list(
    content_list: list,
) -> ObjDetInstanceLabel:
    """Creates an ObjDetInstanceLabel from a list of values.
    Correct order of 'content_list' required:
    idx 0-3: ullr coordinates,
    idx 4: class_name,
    idx 5: class_idx,
    idx 6: prediction score,
    idx 7: rotation"""
    bbox = bounding_box_from_ullr(*content_list[:4])
    class_name: str = content_list[4]
    class_index: Optional[int] = content_list[5]
    score: Optional[float] = content_list[6]
    rotation: int = content_list[7]
    return ObjDetInstanceLabel(
        class_name=class_name,
        bounding_box=bbox,
        class_index=class_index,
        score=score,
        rotation=rotation,
    )


def dict_to_objdet_instance_label(
    data: List[Union[dict, ObjDetInstanceLabel]]
) -> List[ObjDetInstanceLabel]:
    """Converts a list of dicts to a list of ObjDetInstanceLabels"""
    converted_data: List[ObjDetInstanceLabel] = []
    for entry in data:
        if isinstance(entry, dict):
            converted_data.append(ObjDetInstanceLabel(**entry))
        else:
            converted_data.append(entry)
    return converted_data


@define()
class ObjDetImageLabel:  # pylint: disable=too-few-public-methods
    """Labels of all ObjDetInstanceLabels on an image file"""

    filename: str
    img_size: ImageSize
    labels: List[ObjDetInstanceLabel] = field(converter=dict_to_objdet_instance_label)
