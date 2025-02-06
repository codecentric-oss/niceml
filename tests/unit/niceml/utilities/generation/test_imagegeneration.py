from os.path import join, isfile
from tempfile import TemporaryDirectory

import pytest
from PIL import Image
import numpy as np
from pathlib import Path

from niceml.utilities.fsspec.locationutils import LocationConfig
from niceml.utilities.generation.imagegeneration import generate_number_image
from niceml.utilities.imagesize import ImageSize


@pytest.fixture
def tmp_path() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp

@pytest.fixture
def mock_draw_number_on_image(monkeypatch):
    def mock_func(*args, **kwargs):
        return (
            Image.new('RGB', (256, 256)),  # img
            "5",  # text
            type('MockTextLayer', (), {'width': 50, 'height': 50})(),  # text_layer
            (100, 100),  # text_layer_position
            0,  # rotation
            Image.new('L', (256, 256), color=255)  # mask_img
        )
    monkeypatch.setattr('niceml.utilities.generation.drawutils.draw_number_on_image', mock_func)


@pytest.fixture
def random_generator():
    return np.random.default_rng(seed=42)


@pytest.fixture
def bg_image(tmp_path):
    # Create a temporary background image
    img_path = join(tmp_path, "bg_image.png")
    img = Image.new('RGB', (256, 256), color='white')
    img.save(img_path)
    return LocationConfig(uri=tmp_path)


def test_generate_number_image_basic(random_generator, bg_image, mock_draw_number_on_image):
    img, mask_img, metadata = generate_number_image(
        random_generator,
        bg_image_location=bg_image,
        max_number=10,
        img_size=ImageSize(256, 256),
        max_amount=3
    )

    assert isinstance(img, Image.Image)
    assert isinstance(mask_img, Image.Image)
    assert isinstance(metadata, dict)
    assert "image_width" in metadata
    assert "image_height" in metadata
    assert "num_objects" in metadata
    assert "objects" in metadata


def test_generate_number_image_metadata(random_generator, bg_image, mock_draw_number_on_image):
    _, _, metadata = generate_number_image(
        random_generator,
        bg_image_location=bg_image,
        max_number=10,
        img_size=ImageSize(256, 256),
        max_amount=3
    )

    assert metadata["image_width"] == 256
    assert metadata["image_height"] == 256
    assert 1 <= metadata["num_objects"] <= 3
    assert len(metadata["objects"]) == metadata["num_objects"]

    for obj in metadata["objects"]:
        assert "id" in obj
        assert "class" in obj
        assert "x" in obj
        assert "y" in obj
        assert "width" in obj
        assert "height" in obj
        assert "rotation" in obj


def test_generate_number_image_save(random_generator, bg_image, mock_draw_number_on_image, tmp_path):
    location = LocationConfig(uri=str(tmp_path))
    _, _, metadata = generate_number_image(
        random_generator,
        location=location,
        bg_image_location=bg_image,
        max_number=10,
        img_size=ImageSize(256, 256),
        max_amount=3,
        save=True
    )

    assert "file_name" in metadata
    assert "mask_file_name" in metadata
    assert isfile(join(tmp_path, metadata["file_name"]))
    assert isfile(join(tmp_path, metadata["mask_file_name"]))


def test_generate_number_image_no_save_location(random_generator, bg_image, mock_draw_number_on_image):
    with pytest.raises(AttributeError):
        generate_number_image(
            random_generator,
            bg_image_location=bg_image,
            max_number=10,
            img_size=ImageSize(256, 256),
            max_amount=3,
            save=True
        )


def test_generate_number_image_contains_data(random_generator, bg_image, mock_draw_number_on_image):
    _, _, metadata = generate_number_image(
        random_generator,
        bg_image_location=bg_image,
        max_number=10,
        img_size=ImageSize(256, 256),
        max_amount=3
    )

    assert any(key.startswith("count_") for key in metadata.keys())
    count_sum = sum(value for key, value in metadata.items() if key.startswith("count_"))
    assert count_sum == metadata["num_objects"]


@pytest.mark.parametrize("rotate", [True, False])
def test_generate_number_image_rotation(random_generator, bg_image, mock_draw_number_on_image, rotate):
    _, _, metadata = generate_number_image(
        random_generator,
        bg_image_location=bg_image,
        max_number=10,
        img_size=ImageSize(256, 256),
        max_amount=3,
        rotate=rotate
    )

    mock_draw_number_on_image.assert_called_with(
        img=mock_draw_number_on_image.return_value[0],
        random_generator=random_generator,
        max_number=10,
        random_font_size=mock_draw_number_on_image.call_args[1]['random_font_size'],
        img_size=ImageSize(256, 256),
        rotate=rotate,
        mask_img=mock_draw_number_on_image.return_value[5]
    )