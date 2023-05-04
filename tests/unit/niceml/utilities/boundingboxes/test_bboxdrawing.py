from collections import defaultdict

import numpy as np

from niceml.utilities.boundingboxes.bboxconversion import shift_bbox_by_percentage
from niceml.utilities.boundingboxes.bboxdrawing import draw_labels_on_image
from niceml.utilities.boundingboxes.bboxlabeling import ObjDetInstanceLabel
from niceml.utilities.colorutils import Color
from niceml.utilities.imagegeneration import generate_number_image
from niceml.utilities.imagesize import ImageSize


def test_draw_labels_on_image():
    # Given
    img_size = ImageSize(1024, 1024)
    random_generator = np.random.default_rng(seed=42)

    img, _, gt_labels = generate_number_image(
        random_generator=random_generator,
        rotate=True,
        img_size=img_size,
        detection_label=True,
        max_amount=9,
    )
    pred_labels = []

    for index, gt_label in enumerate(gt_labels):
        if index % 3 == 0:
            pred_labels.append(
                ObjDetInstanceLabel(
                    class_name=gt_label.class_name,
                    class_index=gt_label.class_index,
                    bounding_box=shift_bbox_by_percentage(
                        bbox_coords=gt_label.bounding_box.get_absolute_xywh(),
                        percentage=0.2,
                        direction=1,
                        axis=1,
                    ),
                    score=0.0,
                )
            )
        elif index % 3 == 1:
            pred_labels.append(
                ObjDetInstanceLabel(
                    class_name=gt_label.class_name,
                    class_index=gt_label.class_index,
                    bounding_box=shift_bbox_by_percentage(
                        bbox_coords=gt_label.bounding_box.get_absolute_xywh(),
                        percentage=0.3,
                        direction=1,
                        axis=1,
                    ),
                    score=0.0,
                )
            )
        else:
            pred_labels.append(
                ObjDetInstanceLabel(
                    class_name="Other Label",
                    class_index=100,
                    bounding_box=shift_bbox_by_percentage(
                        bbox_coords=gt_label.bounding_box.get_absolute_xywh(),
                        percentage=0.1,
                        direction=1,
                        axis=1,
                    ),
                    score=0.0,
                )
            )

    image = draw_labels_on_image(
        image=img,
        pred_bbox_label_list=pred_labels,
        gt_bbox_label_list=gt_labels,
    )
    by_color = defaultdict(int)

    for pixel in image.getdata():
        by_color[pixel] += 1

    assert image.size == img.size
    assert Color.GREEN in by_color
    assert Color.YELLOW in by_color
    assert Color.BLUE in by_color
    assert Color.RED in by_color
