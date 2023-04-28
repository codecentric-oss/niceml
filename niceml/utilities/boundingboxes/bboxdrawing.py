"""Module for BoundingBoxes / ObjDetInstanceLabels draw functions"""
from typing import List

from PIL import ImageDraw
from PIL.Image import Image as ImageType

from niceml.utilities.boundingboxes.bboxlabeling import ObjDetInstanceLabel
from niceml.utilities.colorutils import Color
from niceml.utilities.imageutils import get_font
from niceml.utilities.instancelabelmatching import get_kind_of_label_match


def draw_bounding_box_on_image(
    label: ObjDetInstanceLabel,
    image: ImageType,
    font_color=Color.BLACK,
):
    """
    Draws a bounding box on an image

    Args:
        label: ObjDetInstanceLabel (bounding box) to draw on the 'image'
        image: image to draw the bounding boxes on
        font_color: font color of the bounding box

    Returns:
        image with the bounding box
    """

    if label.color == Color.BLUE:
        font_color = Color.WHITE

    draw = ImageDraw.Draw(image)

    line_width = int(
        (image.width if image.width >= image.height else image.height) * 0.003
    )
    font_size = int(
        (image.width if image.width >= image.height else image.height) * 0.015
    )

    font = get_font("OpenSans-Regular.ttf", font_size=font_size)

    text = f"{label.class_name}: {label.score:.2f}" if label.score else label.class_name
    text_width, text_height = font.getsize(text)
    x_1, y_1, x_2, y_2 = label.bounding_box.get_absolute_ullr()
    draw.rectangle(
        (x_1 - line_width, y_1 - line_width, x_2 + line_width, y_2 + line_width),
        outline=label.color,
        width=line_width,
    )
    draw.rectangle(
        (
            x_1 - line_width,
            y_1 - (font_size + line_width),
            x_1 + text_width + line_width,
            y_1 - (font_size + line_width) + text_height,
        ),
        fill=label.color,
    )

    draw.text(
        (x_1 - line_width, y_1 - (font_size + line_width)),
        text=text,
        fill=font_color,
        font=font,
    )

    return image


def draw_labels_on_image(  # pylint: disable=too-many-arguments
    image: ImageType,
    pred_bbox_label_list: List[ObjDetInstanceLabel],
    gt_bbox_label_list: List[ObjDetInstanceLabel],
    hide_gt: bool = False,
    hide_gt_over_thresh: bool = False,
    iou_threshold: float = 0.5,
) -> ImageType:
    """
    Draws multiple bounding boxes of ObjDetInstanceLabels on an image

    Args:
        image: image to draw the bounding boxes on
        pred_bbox_label_list: prediction bounding box label information list
        gt_bbox_label_list: ground truth bounding box label information list
        hide_gt: flag to hide the gt labels
        hide_gt_over_thresh: flag to hide the gt labels for the
            predicted bounding boxes with an iou >= iou_threshold
        iou_threshold: iou threshold for label matching

    Returns:
        image with predicted and ground truth bounding boxes
    """
    pred_bbox_visu_label_list: List[ObjDetInstanceLabel]
    gt_bbox_visu_label_list: List[ObjDetInstanceLabel]
    pred_bbox_visu_label_list, gt_bbox_visu_label_list = get_kind_of_label_match(
        pred_label_list=pred_bbox_label_list,
        gt_label_list=gt_bbox_label_list,
        hide_gt_over_thresh=hide_gt_over_thresh,
        iou_threshold=iou_threshold,
    )

    for pred_label in pred_bbox_visu_label_list:
        if pred_label.active:
            image = draw_bounding_box_on_image(image=image, label=pred_label)

    if not hide_gt:
        for gt_label in gt_bbox_visu_label_list:
            if gt_label.active:
                image = draw_bounding_box_on_image(image=image, label=gt_label)
    return image
