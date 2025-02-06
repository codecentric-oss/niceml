"""Module for functions to generate test image dataset"""
import random
from hashlib import sha256
from os.path import join, splitext
from pathlib import Path
from typing import List, Tuple, Union, Optional, Dict, Any

import albumentations as alb
import numpy as np
from PIL import Image
from PIL.Image import Image as ImageType
from attrs import asdict
from tqdm import tqdm

from niceml.utilities.boundingboxes.bboxlabeling import (
    ObjDetImageLabel,
)
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    open_location,
    join_fs_path,
)
from niceml.utilities.generation.drawutils import draw_number_on_image
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.ioutils import read_json, write_image, write_json, read_parquet, list_dir


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

    images = []
    all_labels = []
    classes = set()

    for _ in tqdm(range(sample_count), desc="Generate random number image"):
        image, _, labels = generate_number_image(
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

        images.append(image)
        all_labels.append(labels)

        for label in labels:
            classes.add(label.class_name)

    return list(classes), location


def generate_number_image(
            random_generator,
            location: Union[dict, LocationConfig] = None,
            max_number: int = 10,
            img_size: ImageSize = ImageSize(256, 256),
            rotate: bool = False,
            font_size_min: int = 80,
            font_size_max: int = 140,
            max_amount: int = 3,
            save: bool = False,
            bg_image_location: Optional[LocationConfig] = None,
            image_extensions: Optional[List[str]] = None
    ) -> Tuple[ImageType, ImageType, Dict[str, Any]]:
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
        max_amount: Maximum number of numbers in a single image
        rotate: Whether the drawn numbers should be rotated randomly or not
        save: Save the generated images to given output location
    Returns:
        The generated image, its mask_img and the instance_labels of the numbers
    """
        count_str = "count_{idx}"
        augmentations = get_default_augmentations()
        image_extensions = image_extensions or ['.png', '.jpg', '.jpeg']
        random_font_size = random_generator.integers(font_size_min, font_size_max, 1)[0]
        amount_of_numbers_on_image = random_generator.integers(1, max_amount + 1, 1)[0]

        bg_image_location = bg_image_location or LocationConfig(
            uri=f"{Path(__file__).parent.resolve()}/assets/bg_images")
        with open_location(bg_image_location) as (bg_image_fs, bg_image_dir):
            bg_images = [cur_file for cur_file in
                         list_dir(bg_image_dir, recursive=True, return_full_path=True, file_system=bg_image_fs)
                         if splitext(cur_file)[1] in image_extensions]
            img = Image.open(random.choice(bg_images)).resize(img_size.to_pil_size())

            img_array = np.asarray(img)
            augmented_img = augmentations(image=img_array)["image"]
            img = Image.fromarray(augmented_img)

        mask_img = Image.new("L", img.size, color=255)

        # Initialize the metadata dictionary
        metadata = {
            "image_width": img_size.width,
            "image_height": img_size.height,
            "num_objects": amount_of_numbers_on_image,
            "objects": []
        }

        contains_data = {count_str.format(idx=idx): 0 for idx in range(max_number)}

        for cur_idx in range(amount_of_numbers_on_image):
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

            # Add object metadata to the list
            object_metadata = {
                "id": cur_idx,
                "class": text,
                "x": text_layer_position[0],
                "y": text_layer_position[1],
                "width": text_layer.width,
                "height": text_layer.height,
                "rotation": rotation
            }
            metadata["objects"].append(object_metadata)
            contains_data[count_str.format(idx=text)] += 1

        metadata.update(contains_data)

        if save:
            if not location:
                raise AttributeError(
                    "You have to pass a file_path if you want to save the image"
                )
            file_name: str = sha256(img.tobytes()).hexdigest()[:8]
            with open_location(location) as (cur_fs, root_path):
                write_image(img, join(root_path, file_name + ".png"), cur_fs)
                write_image(mask_img, join(root_path, f"{file_name}_mask.png"), cur_fs)

            metadata["file_name"] = file_name + ".png"
            metadata["mask_file_name"] = f"{file_name}_mask.png"

        return img, mask_img, metadata


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

    df_row = {"identifier": identifier, "label": int(label)}
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
            df_row[f"px_{y}_{x}"] = image[y, x]  # px = pixel
    return df_row


def get_scalar_columns_of_tabular_data(
    tabular_data_location: Union[dict, LocationConfig],
    tabular_data_file_name: str = "train.parq",
) -> List[str]:
    """
    The get_scalar_columns_of_tabular_data function returns a list
    of the scalar columns in the tabular data.

    Args:
        tabular_data_location: Specify the location of the data
        tabular_data_file_name: Specify the name of the parquet file containing tabular data

    Returns:
        A list of the scalar columns in the tabular data
    """
    with open_location(tabular_data_location) as (tabular_data_fs, tabular_data_root):
        tabular_data = read_parquet(
            filepath=join_fs_path(
                tabular_data_fs, tabular_data_root, tabular_data_file_name
            )
        )
        return [
            column for column in tabular_data.columns if column.startswith("px")
        ] + ["label"]


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


def get_default_augmentations():
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

    return augmentations
