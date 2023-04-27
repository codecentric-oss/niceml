"""Module for image utilization"""

from pathlib import Path
from typing import Dict, List, Tuple

import cv2
import numpy as np

# pylint: disable = no-name-in-module
from cv2 import CHAIN_APPROX_SIMPLE, RETR_EXTERNAL, contourArea, findContours
from PIL import Image, ImageFont
from PIL.ImageFont import FreeTypeFont


def stich_images(  # QUEST: still used?
    image_list: List[Image.Image],
    horizontal_count: int,
    vertical_count: int,
    tile_size: Tuple[int, int],
) -> Image.Image:
    """
    Arranges a list of PIL Images in a grid view with a given tile_size.

    image_list: List of images to be arranged
    horizontal_count: Number of images that will be placed horizontally in the stiched image
    vertical_count: Number of images that will be placed vertically in the stiched image
    tile_size: Size of each image tile (width, height)

    Returns:
        All images stitched together in a grid view as one image
    """
    total_width = horizontal_count * tile_size[0]
    total_height = vertical_count * tile_size[1]
    new_image = Image.new("RGB", (total_width, total_height))
    cur_idx = 0
    for vertical_position in range(vertical_count):
        for horizontal_position in range(horizontal_count):
            if cur_idx >= len(image_list):
                break
            cur_img = image_list[cur_idx]
            new_image.paste(
                cur_img,
                box=(
                    horizontal_position * tile_size[0],
                    vertical_position * tile_size[1],
                ),
            )
            cur_idx += 1

    return new_image


def calc_diff_mask(  # QUEST: still used?
    orig_img: np.ndarray, obfuscated_img: np.ndarray, min_dist: float
) -> np.ndarray:
    """Calculates the difference of an `orig_img` and an `obfuscated_img`"""
    diff_array = orig_img - obfuscated_img
    distances = np.linalg.norm(diff_array, axis=-1)
    mask = (distances > min_dist).astype(float)
    return mask


# pylint: disable = no-member
def calc_heatmap(
    prediction: np.ndarray, input_img: np.ndarray
) -> np.ndarray:  # QUEST: still used?
    """Creates a heatmap based on a predicted image and an input image"""
    diff_array = input_img - prediction
    distances = np.linalg.norm(diff_array, axis=-1).astype(np.uint8)
    return cv2.applyColorMap(distances, cv2.COLORMAP_JET)


def get_font(font_name: str, font_size: int = 50) -> FreeTypeFont:
    """Returns a randomly selected `FreeTypeFont` from ten predefined font names"""
    font_path = f"{Path(__file__).parent.resolve()}/assets/fonts/{font_name}"
    return ImageFont.truetype(font=font_path, size=font_size)


def find_contours_in_binary_image(
    binary_image: np.ndarray, min_area: int, max_area: int
) -> List:
    """Find the Contours in a binary Image

    Args:
        binary_image: image to search for contours on
        min_area: minimum area of relevant contours
        max_area: maximum area of relevant contours

    Returns:
        Found contours within the relevant area range
    """
    contours = findContours(binary_image, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)[0]
    return [
        contour for contour in contours if min_area <= contourArea(contour) <= max_area
    ]


# pylint: disable = no-member
def binarize_multichannel_image(
    image_index: np.ndarray, image_scores: np.ndarray, threshold: float
) -> Tuple[Dict[str, np.ndarray], np.ndarray]:
    """
    Binarize (0,1) a multichannel image holding prediction information based on a threshold.
    Returns one binarized image per class and an overall mask with prediction scores above
    the threshold.

    Args:
        image_index: np.ndarray
            numpy array with the shape (image.height, image.width) filled
            with the predicted class index of each pixel
        image_scores: np.ndarray
            numpy array with the shape (image.height, image.width) filled
            with a prediction score (0.0-1.0) of each pixel
        threshold: float
            threshold to create a mask with a prediction score > threshold

    Returns:
        binary_multichannel_images: Dict[str, np.array]
            Dictionary of binarized images per class
        scores_mask: np.ndarray
            mask including information where the prediction is above threshold
    """
    binary_multichannel_images: Dict[str, np.ndarray] = {}
    scores_mask = cv2.threshold(image_scores, threshold, 1, cv2.THRESH_BINARY,)[
        1
    ].astype(np.uint8)

    masked_index = image_index * scores_mask

    class_idx_list = np.unique(masked_index)

    for class_idx in class_idx_list:
        if class_idx > 0:
            cur_idx_img = np.copy(masked_index)
            cur_idx_img[masked_index != class_idx] = 0
            curr_binary_mask = ((cur_idx_img / class_idx) * 255).astype(np.uint8)
            binary_multichannel_images[str(class_idx)] = curr_binary_mask
    return binary_multichannel_images, scores_mask
