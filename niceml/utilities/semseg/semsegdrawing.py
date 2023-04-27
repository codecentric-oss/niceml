"""Module for error mask (SemSegInstanceLabel) draw functions"""
from typing import List

from PIL import Image
from PIL.Image import Image as ImageType

from niceml.utilities.semseg.semseginstancelabeling import SemSegInstanceLabel


def draw_error_mask_on_image(
    label: SemSegInstanceLabel,
    image: ImageType,
) -> ImageType:
    """
    Draws an error mask of a SemSegInstanceLabel on an image

    Args:
        label: label (error mask) to draw on the image
        image: image to draw the error masks on

    Returns:
        image with the error mask
    """

    color_image = Image.new("RGB", image.size, label.color)
    mask_input = label.mask
    mask_input[mask_input == 255] = 100
    mask = Image.fromarray(mask_input)
    mask = mask.convert("L")
    image = Image.composite(color_image, image, mask)
    return image


def draw_labels_on_image(  # pylint: disable=too-many-arguments
    image: ImageType,
    pred_error_mask_label_list: List[SemSegInstanceLabel],
    gt_error_mask_label_list: List[SemSegInstanceLabel],
    hide_gt: bool = False,
) -> ImageType:
    """

    Draws multiple prediction and ground truth error mask labels
    (SemSegInstanceLabel) on an image

    Args:
        image: image to draw the error masks on
        pred_error_mask_label_list: list of prediction error mask labels
        gt_error_mask_label_list: list of ground truth error mask labels
        hide_gt: flag to hide the gt labels

    Returns:
        Image with predicted and ground truth error masks
    """

    for pred_label in pred_error_mask_label_list:
        if pred_label.active:
            image = draw_error_mask_on_image(image=image, label=pred_label)

    if not hide_gt:
        for gt_label in gt_error_mask_label_list:
            if gt_label.active:
                image = draw_error_mask_on_image(image=image, label=gt_label)
    return image
