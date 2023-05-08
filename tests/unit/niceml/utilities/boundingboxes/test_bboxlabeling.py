import pytest

from niceml.utilities.boundingboxes.bboxlabeling import (
    ObjDetInstanceLabel,
    obj_instance_factory_from_content_list,
)
from niceml.utilities.boundingboxes.boundingbox import BoundingBox


@pytest.mark.parametrize(
    "obj_instance_label",
    [
        ObjDetInstanceLabel(
            class_name="one", bounding_box=BoundingBox(100, 200, 300, 400)
        ),
        ObjDetInstanceLabel(
            class_name="two", bounding_box=BoundingBox(80, 100, 400, 350), class_index=3
        ),
        ObjDetInstanceLabel(
            class_name="three",
            bounding_box=BoundingBox(100.5, 200.3, 300, 400),
            class_index=0,
            score=100,
        ),
        ObjDetInstanceLabel(
            class_name="", bounding_box=BoundingBox(70, 80, 55, 10), rotation=10
        ),
    ],
)
def test_obj_instance_labeling_conversion(
    obj_instance_label: ObjDetInstanceLabel,
):
    content_list = obj_instance_label.to_content_list()
    new_obj_instance_label = obj_instance_factory_from_content_list(content_list)
    assert obj_instance_label == new_obj_instance_label
