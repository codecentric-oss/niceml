import json
from os.path import join
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import pytest
from attrs import asdict

from niceml.utilities.boundingboxes.bboxlabeling import (
    ObjDetImageLabel,
    ObjDetInstanceLabel,
)
from niceml.utilities.boundingboxes.boundingbox import BoundingBox
from niceml.utilities.imagegeneration import generate_test_images
from niceml.utilities.imagesize import ImageSize


@pytest.fixture()
def created_test_image_path(tmp_dir) -> Tuple[List[str], dict]:
    # config
    sample_count = 10
    seed = 42
    max_number = 8
    img_size = ImageSize(256, 256)
    font_size_min = 40
    font_size_max = 80
    detection_labels = True
    max_amount = 4
    rotate = True
    save = True

    classes, output_location = generate_test_images(
        location={"uri": tmp_dir},
        sample_count=sample_count,
        seed=seed,
        max_number=max_number,
        img_size=img_size,
        font_size_min=font_size_min,
        font_size_max=font_size_max,
        detection_labels=detection_labels,
        max_amount=max_amount,
        rotate=rotate,
        save=save,
    )
    return classes, output_location


def objdet_image_label_path(file_path) -> str:
    name = "test_label"
    filename = "test.mask_image"
    img_size = ImageSize(256, 256)

    labels = [get_random_objdet_instance_label() for _ in range(3)]

    data = ObjDetImageLabel(filename=filename, img_size=img_size, labels=labels)

    path = Path(file_path)
    path.mkdir(exist_ok=True, parents=True)

    with open(f"{path}/{name}.json", "w", encoding="utf-8") as file:
        json.dump(asdict(data), file)

    return join(file_path, f"{name}.json")


def get_random_objdet_instance_label() -> ObjDetInstanceLabel:
    random_generator = np.random.default_rng(seed=42)
    random_img_size = ImageSize(
        height=random_generator.integers(10, 1024, dtype=int),
        width=random_generator.integers(10, 1024, dtype=int),
    )

    class_name = str(random_generator.integers(0, 10))

    bounding_box = get_random_bounding_box(
        img_size=random_img_size, random_generator=random_generator
    )
    class_index = random_generator.integers(10, dtype=int)
    rotation = False

    return ObjDetInstanceLabel(
        class_name=class_name,
        bounding_box=bounding_box,
        class_index=class_index,
        rotation=rotation,
    )


def get_random_bounding_box(
    img_size: ImageSize,
    random_generator=None,
    bbox_width: Optional[int] = None,
    bbox_height: Optional[int] = None,
) -> BoundingBox:
    if random_generator is None:
        random_generator = np.random.default_rng(seed=42)

    rand_height = (
        random_generator.integers(1, img_size.height, dtype=int)
        if bbox_height is None
        else bbox_height
    )
    rand_width = (
        random_generator.integers(1, img_size.width, dtype=int)
        if bbox_width is None
        else bbox_width
    )

    rand_x_pos = random_generator.integers(0, img_size.width - rand_width, dtype=int)
    rand_y_pos = random_generator.integers(0, img_size.height - rand_height, dtype=int)

    return BoundingBox(
        x_pos=rand_x_pos, y_pos=rand_y_pos, width=rand_width, height=rand_height
    )
