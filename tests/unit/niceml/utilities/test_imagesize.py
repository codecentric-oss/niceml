import numpy as np
import pytest

from niceml.utilities.imagesize import ImageSize, ImageSizeDivisionError


def test_to_numpy_shape():
    image_size = ImageSize(width=100, height=200)
    assert image_size.to_numpy_shape() == (200, 100)


def test_to_pil_size():
    image_size = ImageSize(width=100, height=200)
    assert image_size.to_pil_size() == (100, 200)


def test_str():
    image_size = ImageSize(width=100, height=200)
    assert str(image_size) == "[100,200]"


def test_truediv():
    image_size = ImageSize(width=100, height=200)
    image_size2 = image_size / 2
    assert image_size2.width == 50 and image_size2.height == 100


def test_mul():
    image_size = ImageSize(width=100, height=200)
    image_size2 = image_size * 2
    assert image_size2.width == 200 and image_size2.height == 400


def test_get_division_factor():
    image_size = ImageSize(width=100, height=200)
    image_size2 = ImageSize(width=200, height=400)
    assert image_size.get_division_factor(image_size2) == 0.5


def test_get_division_factor_raises_error():
    image_size = ImageSize(width=100, height=200)
    image_size2 = ImageSize(width=200, height=300)
    with pytest.raises(ImageSizeDivisionError):
        image_size.get_division_factor(image_size2)


def test_le():
    image_size = ImageSize(width=100, height=200)
    image_size2 = ImageSize(width=200, height=400)
    assert image_size <= image_size2


def test_le_raises_error():
    image_size = ImageSize(width=100, height=200)
    image_size2 = ImageSize(width=200, height=300)
    with pytest.raises(ImageSizeDivisionError):
        image_size <= image_size2  # pylint: disable=pointless-statement


def test_np_array_has_same_size():
    image_size = ImageSize(width=100, height=200)
    np_array = np.zeros((200, 100, 3))
    assert image_size.np_array_has_same_size(np_array)


def test_np_array_has_same_size_false():
    image_size = ImageSize(width=100, height=200)
    np_array = np.zeros((200, 101, 3))
    assert not image_size.np_array_has_same_size(np_array)


def test_create_with_same_aspect_ratio():
    image_size = ImageSize(width=100, height=200)
    image_size2 = image_size.create_with_same_aspect_ratio(width=200)
    assert image_size2.width == 200 and image_size2.height == 400


def test_create_with_same_aspect_ratio_raises_error():
    image_size = ImageSize(width=100, height=200)
    with pytest.raises(ImageSizeDivisionError):
        image_size.create_with_same_aspect_ratio(width=200, height=500)


def test_create_with_same_aspect_ratio2():
    image_size = ImageSize(width=100, height=200)
    image_size2 = image_size.create_with_same_aspect_ratio(height=400)
    assert image_size2.width == 200 and image_size2.height == 400


def test_create_with_same_aspect_ratio2_raises_error():
    image_size = ImageSize(width=100, height=200)
    with pytest.raises(ValueError):
        image_size.create_with_same_aspect_ratio()


def test_creation_from_pil_image():
    from PIL import Image

    image = Image.new("RGB", (100, 200))
    image_size = ImageSize.from_pil_image(image)
    assert image_size.width == 100 and image_size.height == 200
    image_size = ImageSize.from_pil_size(image.size)
    assert image_size.width == 100 and image_size.height == 200
