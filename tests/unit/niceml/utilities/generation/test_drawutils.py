import pytest
import numpy as np
from PIL import ImageFont, Image, ImageDraw


from niceml.utilities.generation.drawutils import (
    get_random_position,
    get_random_color,
    get_rand_font,
    get_rand_rotation,
    ImageSize,
    crop_text_layer_to_text
)


@pytest.fixture
def random_generator():
    """Fixture to provide a consistent random generator for tests."""
    return np.random.default_rng(seed=42)


def test_get_random_position(random_generator):
    """
    Test the get_random_position function.

    This test checks if the function returns coordinates within the expected range,
    both with and without a specified font size.
    """
    img_size = ImageSize(256, 256)

    # Test without font size
    x, y = get_random_position(random_generator, img_size)
    assert 0 <= x < img_size.width
    assert 0 <= y < img_size.height

    # Test with font size
    font_size = 50
    x, y = get_random_position(random_generator, img_size, font_size)
    assert 0 <= x < img_size.width - font_size
    assert 0 <= y < img_size.height - font_size


def test_get_random_color(random_generator):
    """
    Test the get_random_color function.

    This test checks if the function returns a valid RGB tuple.
    """
    color = get_random_color(random_generator)
    assert isinstance(color, tuple)
    assert len(color) == 3
    assert all(0 <= c <= 255 for c in color)


def test_get_rand_font(random_generator):
    """
    Test the get_rand_font function.

    This test checks if the function returns a FreeTypeFont object
    with the specified font size.
    """
    font_size = 50
    font = get_rand_font(random_generator, font_size)
    assert isinstance(font, ImageFont.FreeTypeFont)
    assert font.size == font_size


def test_get_rand_rotation(random_generator):
    """
    Test the get_rand_rotation function.

    This test checks if the function returns a rotation value
    within the expected range.
    """
    rotation = get_rand_rotation(random_generator)
    assert isinstance(rotation, int)
    assert 0 <= rotation < 360


def create_test_image(size, text_box):
    """Helper function to create a test image with text"""
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle(text_box, fill=(255, 255, 255, 255))
    return image


@pytest.mark.parametrize("image_size,text_box,expected_size", [
    ((100, 100), (25, 25, 75, 75), (51, 51)),
    ((200, 100), (50, 25, 150, 75), (101, 51)),
    ((100, 200), (25, 50, 75, 150), (51, 101)),
    ((100, 100), (0, 0, 99, 99), (100, 100)),
    ((100, 100), (40, 40, 60, 60), (21, 21)),
])
def test_crop_text_layer_to_text(image_size, text_box, expected_size):
    """
    Test the crop_text_layer_to_text function with various image and text sizes.

    This test creates images with known text areas and checks if the cropping
    results in the expected image size.
    """
    test_image = create_test_image(image_size, text_box)
    cropped_image = crop_text_layer_to_text(test_image)
    assert cropped_image.size == expected_size


def test_crop_text_layer_to_text_empty_image():
    """
    Test the crop_text_layer_to_text function with an empty (fully transparent) image.

    This test checks if the function handles the edge case of an image with no text correctly.
    """
    empty_image = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
    with pytest.raises(IndexError):
        crop_text_layer_to_text(empty_image)


def test_crop_text_layer_to_text_full_image():
    """
    Test the crop_text_layer_to_text function with a fully filled image.

    This test checks if the function returns the original image when it's fully filled.
    """
    full_image = Image.new('RGBA', (100, 100), (255, 255, 255, 255))
    cropped_image = crop_text_layer_to_text(full_image)
    assert cropped_image.size == full_image.size


def test_crop_text_layer_to_text_single_pixel():
    """
    Test the crop_text_layer_to_text function with a single non-transparent pixel.

    This test checks if the function correctly crops to a single pixel.
    """
    image = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
    image.putpixel((50, 50), (255, 255, 255, 255))
    cropped_image = crop_text_layer_to_text(image)
    assert cropped_image.size == (1, 1)


def test_crop_text_layer_to_text_preserves_content():
    """
    Test that crop_text_layer_to_text preserves the content of the cropped area.

    This test checks if the function correctly preserves the pixel values in the cropped area.
    """
    original_image = create_test_image((100, 100), (25, 25, 75, 75))
    cropped_image = crop_text_layer_to_text(original_image)

    # Check if all non-transparent pixels are preserved
    original_array = np.array(original_image)
    cropped_array = np.array(cropped_image)
    assert np.all(original_array[25:76, 25:76] == cropped_array)