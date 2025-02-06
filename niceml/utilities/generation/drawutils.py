"""helper functions for generating data"""
from typing import Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageOps
from PIL.Image import Image as ImageType
from PIL.ImageFont import FreeTypeFont

from niceml.utilities.imagesize import ImageSize
from niceml.utilities.imageutils import get_font


def draw_number_on_image(  # noqa: PLR0913
    img: ImageType,
    random_generator,
    max_number: int,
    random_font_size: int,
    img_size: ImageSize,
    rotate: bool,
    mask_img: ImageType,
) -> Tuple[ImageType, str, ImageType, Tuple[int, int], int, ImageType]:
    """
    Draws a number on an image, rotates it randomly (if rotate == True) and
    returns text information (text,text layer, text layer position)
    Args:
        img: image to draw the numbers on
        random_generator: Generator of random numbers
        max_number: Maximum number of digits that can be generated
        random_font_size: Size of numbers in image
        img_size: Size of the generated image
        rotate: Whether the number should be rotated randomly or not
        mask_img: Image with label information

    Returns:
        Tuple of 6 parameters: The image, the drawn number, the text_layer, the position of
        the number on the image, rotation of the drawn number, mask_img with updated label
        information.
    """
    number = int(random_generator.integers(0, max_number, 1)[0])
    number_to_draw = str(number)

    text_layer = Image.new(
        "L", (int(random_font_size * 1.4), int(random_font_size * 1.4))
    )

    draw = ImageDraw.Draw(text_layer)
    number_position = get_random_position(
        random_generator=random_generator,
        font_size=random_font_size,
        img_size=img_size,
    )
    draw.text(
        xy=(0, 0),
        text=number_to_draw,
        fill=255,
        font=get_rand_font(
            random_generator=random_generator, font_size=random_font_size
        ),
    )

    if rotate:
        rotation = get_rand_rotation(random_generator=random_generator)
        text_layer = crop_text_layer_to_text(text_layer.rotate(rotation, expand=True))
    else:
        rotation = None
        text_layer = crop_text_layer_to_text(text_layer)

    img.paste(
        ImageOps.colorize(
            text_layer,
            black="black",
            white=get_random_color(random_generator=random_generator),
        ),
        number_position,
        text_layer,
    )
    text_classidx_img = Image.new("L", text_layer.size, color=number)
    mask_img.paste(
        text_classidx_img,
        number_position,
        text_layer,
    )

    return img, number_to_draw, text_layer, number_position, rotation, mask_img


def crop_text_layer_to_text(text_layer: Image.Image) -> Image.Image:
    """
    Takes in a text layer (image object) and returns the same image, but cropped to only include
    the number

    Args:
        text_layer: image layer including text and is otherwise transparent (0)

    Returns:
        cropped version of text_layer with only the number part of the image object
    """
    # Convert image to numpy array for faster processing
    arr = np.array(text_layer)

    # Find rows and columns that are not all zero
    rows = np.any(arr != 0, axis=1)
    cols = np.any(arr != 0, axis=0)

    # Find the bounding box
    ymin, ymax = np.where(rows)[0][[0, -1]]
    xmin, xmax = np.where(cols)[0][[0, -1]]

    # Crop the image
    return text_layer.crop((xmin, ymin, xmax + 1, ymax + 1))


def get_random_position(
    random_generator, img_size: ImageSize = ImageSize(256, 256), font_size: int = None
) -> Tuple[int, int]:
    """Returns a random x and y coordinate inside an image size
    with a padding of a given font size"""

    random_x = random_generator.integers(
        0, img_size.width if font_size is None else (img_size.width - font_size)
    )
    random_y = random_generator.integers(
        0, img_size.height if font_size is None else (img_size.height - font_size)
    )
    return random_x, random_y


def get_random_color(random_generator) -> Tuple[int, int, int]:
    """Returns a tuple representing random RGB values"""
    return tuple(random_generator.integers(0, 255, 3))


def get_rand_font(random_generator, font_size: int = 50) -> FreeTypeFont:
    """Returns a randomly selected `FreeTypeFont` from ten predefined font names"""

    rand_font = random_generator.integers(0, 9, 1)[0]
    fonts = [
        "OpenSans-Regular.ttf",
        "DMMono-Regular.ttf",
        "OxygenMono-Regular.ttf",
        "RobotoMono-Regular.ttf",
        "OpenSans-Regular.ttf",
        "Oswald-Regular.ttf",
        "Ubuntu-Regular.ttf",
        "Rubik-Regular.ttf",
        "Heebo-Regular.ttf",
        "Karla-Regular.ttf",
        "Dosis-Regular.ttf",
    ]
    return get_font(font_name=fonts[rand_font], font_size=font_size)


def get_rand_rotation(random_generator) -> int:
    """Returns a random rotation between 0 and 360"""
    return int(random_generator.integers(0, 360, 1)[0])
