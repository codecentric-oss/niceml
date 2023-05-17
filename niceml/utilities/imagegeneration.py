"""Module for functions to generate test image dataset"""
import random
from copy import copy
from dataclasses import dataclass
from hashlib import sha256
from os.path import join
from pathlib import Path
from typing import List, Tuple, Union, Optional

import albumentations as alb
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from PIL.Image import Image as ImageType
from PIL.ImageFont import FreeTypeFont
from attrs import asdict
from tqdm import tqdm

from niceml.utilities.boundingboxes.bboxlabeling import (
    ObjDetImageLabel,
    ObjDetInstanceLabel,
)
from niceml.utilities.boundingboxes.boundingbox import BoundingBox
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_location_w_path,
    open_location,
)
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.imageutils import get_font
from niceml.utilities.ioutils import read_json, write_image, write_json


# pylint: disable=too-many-instance-attributes
# Ten is reasonable in this case.
@dataclass
class NumberDataGenerator:
    """Generator of images with numbers for an object detection test dataset"""

    location: Union[dict, LocationConfig]
    sample_count: int
    max_number: int
    img_size: ImageSize
    font_size_min: int
    font_size_max: int
    detection_labels: bool
    max_amount: int
    rotate: bool
    sub_dir: str = ""
    seed: Optional[int] = None

    def generate_images(self) -> dict:
        """Generate images based on a configuration (self).
        Returns image_location to generated images."""

        if len(self.sub_dir) > 0:
            location = join_location_w_path(self.location, self.sub_dir)
        else:
            location = self.location

        _, output_location = generate_test_images(
            location=location,
            sample_count=self.sample_count,
            seed=self.seed,
            max_number=self.max_number,
            img_size=self.img_size,
            font_size_min=self.font_size_min,
            font_size_max=self.font_size_max,
            detection_labels=self.detection_labels,
            rotate=self.rotate,
        )

        if isinstance(output_location, LocationConfig):
            output_location = asdict(output_location)
        return output_location


def generate_test_images(  # noqa: PLR0913
    location: Union[dict, LocationConfig],
    sample_count: int,
    seed: Optional[int] = 1234,
    max_number=10,
    img_size: ImageSize = ImageSize(256, 256),
    font_size_min: int = 80,
    font_size_max: int = 140,
    detection_labels: bool = False,
    max_amount: int = 3,
    rotate: bool = False,
    save: bool = True,
) -> Tuple[List[str], Union[dict, LocationConfig]]:
    """
    Wrapper function for 'generate_number_image', which creates a series of generated images
    with random numbers on them and saves them, if save == True, including the label
    information (= position of numbers).
    Returns a list of created classes and the output_location

    Args:
        location: Output location of the image and its label
        sample_count: Number of images to be generated
        seed: Seed for the random number generator
        max_number: Maximum number of digits that can be generated
        img_size: Size of the generated image
        font_size_min: Minimum font size of the numbers in the image
        font_size_max: Maximum font size of the numbers in the image
        detection_labels: Determine if the label should be usable for object detection
        max_amount: Maximum number of numbers in a single image
        rotate: Whether the drawn numbers should be rotated randomly or not
        save: Save the generated images to given output location

    Returns:
        List of label classes and a location configuration
    """

    random_generator = np.random.default_rng(seed=seed)
    random.seed(seed)  # Setting the seed of `random` is required by albumentation
    images, _, labels = list(
        map(
            list,
            zip(
                *[
                    generate_number_image(
                        random_generator=random_generator,
                        max_number=max_number,
                        img_size=img_size,
                        font_size_min=font_size_min,
                        font_size_max=font_size_max,
                        detection_label=detection_labels,
                        max_amount=max_amount,
                        rotate=rotate,
                        location=location,
                        save=save,
                    )
                    for _ in tqdm(
                        range(sample_count), desc="Generate random number image"
                    )
                ]
            ),
        )
    )

    classes = []
    for _, labels_of_curr_images in zip(images, labels):
        classes += [label.class_name for label in labels_of_curr_images]

    return list(set(classes)), location


def generate_number_image(  # noqa: PLR0913
    random_generator,
    location: Union[dict, LocationConfig] = None,
    max_number: int = 10,
    img_size: ImageSize = ImageSize(256, 256),
    rotate: bool = False,
    font_size_min: int = 80,
    font_size_max: int = 140,
    detection_label: bool = False,
    max_amount: int = 3,
    save: bool = False,
) -> Tuple[ImageType, ImageType, List[Union[ObjDetInstanceLabel, None]]]:
    """
    Creates a series of generated images with random numbers on them and saves them,
    if save == True, including the label information (= position of numbers).
    Images are either a random color or a thumbnail image.
    Returns a list of created classes and the output_location.

    Args:
        random_generator: Generator of random numbers
        location: Output location of the image and its label
        max_number: Maximum number of digits that can be generated
        img_size: Size of the generated image
        font_size_min: Minimum font size of the numbers in the image
        font_size_max: Maximum font size of the numbers in the image
        detection_label: Determine if the label should be usable for object detection
        max_amount: Maximum number of numbers in a single image
        rotate: Whether the drawn numbers should be rotated randomly or not
        save: Save the generated images to given output location
    Returns:
        The generated image, its mask_img and the instance_labels of the numbers
    """

    augmentations = alb.Compose(
        [
            alb.ShiftScaleRotate(p=0.5),
            alb.HorizontalFlip(p=0.5),
            alb.RandomBrightnessContrast(p=0.3),
            alb.OneOf(
                [
                    alb.OpticalDistortion(p=0.3),
                    alb.GridDistortion(p=0.1),
                ],
                p=0.2,
            ),
            alb.OneOf(
                [
                    alb.CLAHE(clip_limit=2),
                    alb.Sharpen(),
                    alb.Emboss(),
                    alb.RandomBrightnessContrast(),
                ],
                p=0.3,
            ),
            alb.HueSaturationValue(p=0.3),
            alb.PiecewiseAffine(scale=0.3, p=0.35),
        ]
    )

    instance_labels: List[Union[ObjDetInstanceLabel, None]] = []
    random_font_size = random_generator.integers(font_size_min, font_size_max, 1)[0]
    amount_of_numbers_on_image = random_generator.integers(1, max_amount + 1, 1)[0]

    bg_image_paths = [
        file
        for file in Path(
            f"{Path(__file__).parent.resolve()}/assets/bg_images"
        ).iterdir()
        if file.is_file()
    ]
    random_bg = random_generator.integers(0, len(bg_image_paths) - 1, 1)[0]
    img = Image.open(bg_image_paths[random_bg]).resize(img_size.to_pil_size())

    img_array = np.asarray(img)
    augmented_img = augmentations(image=img_array)["image"]
    img = Image.fromarray(augmented_img)
    
    mask_img = Image.new("L", img.size, color=255)
    for _ in range(amount_of_numbers_on_image):
        (
            img,
            text,
            text_layer,
            text_layer_position,
            rotation,
            mask_img,
        ) = draw_number_on_image(
            img=img,
            random_generator=random_generator,
            max_number=max_number,
            random_font_size=random_font_size,
            img_size=img_size,
            rotate=rotate,
            mask_img=mask_img,
        )
        instance_labels.append(
            create_objdet_instance_label_from_text_label(
                **{
                    "text_layer_position": text_layer_position,
                    "class_name": text,
                    "img_size": img_size,
                    "bounding_box_width": text_layer.width,
                    "bounding_box_height": text_layer.height,
                    "rotation": rotation,
                }
                if detection_label
                else {"class_name": text}
            )
        )

    if save:
        if not location:
            raise AttributeError(
                "You have to pass a file_path if you want to save the image"
            )
        file_name: str = sha256(img.tobytes()).hexdigest()[:8]
        with open_location(location) as (cur_fs, root_path):
            write_image(img, join(root_path, file_name + ".png"), cur_fs)
            write_image(mask_img, join(root_path, f"{file_name}_mask.png"), cur_fs)
        if detection_label:
            label = ObjDetImageLabel(
                filename=join(f"{file_name}.json"),
                img_size=img_size,
                labels=instance_labels,
            )

            save_image_label_as_json(data=label, location=location, name=file_name)

    return img, mask_img, instance_labels


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


def create_objdet_instance_label_from_text_label(  # noqa: PLR0913
    class_name: str,
    img_size: ImageSize = None,
    bounding_box_width: int = None,
    bounding_box_height: int = None,
    text_layer_position: Tuple[int, int] = None,
    rotation: int = None,
) -> ObjDetInstanceLabel:
    """
    Creates an instance of an `ObjDetInstanceLabel` including bounding box
    information if all parameters are given. Otherwise, only the class_name is included.

    Args:
        class_name: Name of the class to label
        img_size: Size of image the label fits to
        bounding_box_width: Width of bounding box
        bounding_box_height: Height of bounding box
        text_layer_position: Position of text to be labeled on the image
        rotation: Rotation of the text

    Returns:
        ObjDetInstanceLabel with class information and,
        if given,position of the label (bounding box)
    """

    if None in (bounding_box_width, bounding_box_height, img_size, text_layer_position):
        return ObjDetInstanceLabel(class_name=class_name, bounding_box=None)

    bounding_box = BoundingBox(
        x_pos=int(text_layer_position[0]),
        y_pos=int(text_layer_position[1]),
        width=bounding_box_width,
        height=bounding_box_height,
    )

    return ObjDetInstanceLabel(
        class_name=class_name, bounding_box=bounding_box, rotation=rotation
    )


def convert_image_to_df_row(
    identifier: str,
    label: str,
    image: Union[np.ndarray, ImageType],
    target_size: Optional[Union[Tuple[int, int], ImageSize]] = None,
) -> dict:
    """
    Takes an image and converts it to a row of data for a pandas DataFrame.

    Args:
        identifier: str: Value to identify the image
        label: str: Target label of the image
        image: Union[np.ndarray,ImageType]: Image to convert into a dataframe row
        target_size: Optional[Union[Tuple[int, int]: Specify the target size of the image
    Returns:
        A dictionary representing a dataframe row
    """
    df_row = {"identifier": identifier, "label": label}
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    image = image.convert(mode="L")
    image = np.asarray(image, dtype=np.uint8)

    if target_size:
        if isinstance(target_size, ImageSize):
            target_size = target_size.to_numpy_shape()
        image = np.resize(image, target_size)
    else:
        target_size = image.shape

    for y in range(target_size[0]):
        for x in range(target_size[1]):
            df_row[f"px_{y}_{x}"] = image[y, x]
    return df_row


def crop_text_layer_to_text(text_layer: ImageType) -> ImageType:
    """
    Takes in a text layer (image object) and returns the same image, but cropped to only include
    the number

    Args:
        text_layer: image layer including text and is otherwise transparent (0)

    Returns:
        cropped version of text_layer with only the number part of the image object
    """
    pixels = text_layer.load()
    width, height = text_layer.size
    max_x = max_y = 0
    min_y = copy(height)
    min_x = copy(width)

    # Find the corners that bound the number by looking for non-transparent pixels
    for x_pos in range(width):
        for y_pos in range(height):
            curr_pixel = pixels[x_pos, y_pos]
            if curr_pixel != 0:
                min_x = min(x_pos, min_x)
                min_y = min(y_pos, min_y)
                max_x = max(x_pos, max_x)
                max_y = max(y_pos, max_y)

    return text_layer.crop((min_x, min_y, max_x, max_y))


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
    """Returns a random rotation between 10 and 350"""
    return int(random_generator.integers(10, 350, 1)[0])


def save_image(img: ImageType, name: str, file_path: str):
    """Saves an image to a file_path and creates folders if not exist"""
    path = Path(f"{file_path}")
    path.mkdir(exist_ok=True, parents=True)
    img.save(f"{path}/{name}.png")


def save_image_label_as_json(
    data: ObjDetImageLabel, location: Union[dict, LocationConfig], name: str
):
    """Saves an ObjDetImageLabel to a file_path and creates folders if not exist"""
    with open_location(location) as (cur_fs, root_path):
        write_json(asdict(data), join(root_path, f"{name}.json"), cur_fs)


def load_label_from_json(
    location: Union[dict, LocationConfig], filename: str
) -> ObjDetImageLabel:
    """Loads an object detection label from a file_path"""
    with open_location(location) as (cur_fs, root_path):
        data = read_json(join(root_path, filename), cur_fs)
        label = ObjDetImageLabel(**data)
    return label
