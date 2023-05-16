from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageDraw

from niceml.utilities.boundingboxes.bboxlabeling import (
    ObjDetImageLabel,
    ObjDetInstanceLabel,
)
from niceml.utilities.imagegeneration import (
    crop_text_layer_to_text,
    generate_number_image,
    generate_test_images,
    load_label_from_json,
)
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.imageutils import get_font
from niceml.utilities.splitutils import clear_folder
from tests.unit.niceml.data.conftest import objdet_image_label_path

import numpy as np
import pytest

from niceml.utilities.imagegeneration import convert_image_to_df_row


def test_single_image_generation():
    # Given
    img_size = ImageSize(1024, 1024)
    random_generator = np.random.default_rng(seed=42)

    # When
    img, _, labels = generate_number_image(
        random_generator=random_generator,
        rotate=True,
        img_size=img_size,
        detection_label=True,
        max_amount=3,
    )
    # Then
    arr_sum = np.array(img, dtype=np.uint8).sum(axis=2)
    unique_color = np.unique(arr_sum)

    for label in labels:
        assert label.class_name in ["8", "7", "3"]
    assert img_size.to_pil_size() == img.size
    assert unique_color.size > 1


def test_multi_image_generation(tmp_dir):
    # Given
    sample_count = 25
    detection_labels = True
    seed = 1234
    max_number = 20
    img_size = ImageSize(256, 256)
    save = True

    tmp_location = {"uri": tmp_dir}
    clear_folder(tmp_location)
    # When
    generate_test_images(
        location=tmp_location,
        sample_count=sample_count,
        seed=seed,
        max_number=max_number,
        img_size=img_size,
        detection_labels=detection_labels,
        save=save,
    )

    # Then
    path = Path(tmp_dir)
    files = [x for x in path.glob("**/*") if x.is_file()]
    assert len(files) == ((sample_count * 3) if detection_labels else sample_count)


def test_load_label_from_json(tmp_dir):
    # Given
    file_path = objdet_image_label_path(file_path=tmp_dir)

    # When
    objdet_image_label: ObjDetImageLabel = load_label_from_json(
        location={"uri": file_path}, filename=""
    )

    # Then
    # pylint:disable=not-an-iterable
    for instance_label in objdet_image_label.labels:
        assert isinstance(instance_label, ObjDetInstanceLabel)


def test_crop_text_layer_to_text():
    font_size = 120

    font = get_font(font_name="OpenSans-Regular.ttf", font_size=font_size)

    text_layer = Image.new("L", (int(font_size * 1.4), int(font_size * 1.4)))

    draw = ImageDraw.Draw(text_layer)

    draw.text(xy=(0, 0), text="2", fill=255, font=font)

    text_layer = crop_text_layer_to_text(text_layer)

    assert (57, 87) == text_layer.size


@pytest.mark.parametrize(
    "identifier, label, image, target_size, expected_output",
    [
        (
            "test_image",
            "positive",
            np.zeros((4, 4), dtype=np.uint8),
            (2, 2),
            {
                "identifier": "test_image",
                "label": "positive",
                "px_0_0": 0,
                "px_0_1": 0,
                "px_1_0": 0,
                "px_1_1": 0,
            },
        ),
        (
            "test_image_2",
            "negative",
            np.ones((3, 3), dtype=np.uint8),
            None,
            {
                "identifier": "test_image_2",
                "label": "negative",
                "px_0_0": 1,
                "px_0_1": 1,
                "px_0_2": 1,
                "px_1_0": 1,
                "px_1_1": 1,
                "px_1_2": 1,
                "px_2_0": 1,
                "px_2_1": 1,
                "px_2_2": 1,
            },
        ),
    ],
)
def test_convert_image_to_df_row(
    identifier: str,
    label: str,
    image: np.ndarray,
    target_size: Optional[Tuple],
    expected_output: dict,
):
    # call the function with the test data
    df_row = convert_image_to_df_row(identifier, label, image, target_size)

    # check the output
    assert df_row == expected_output
