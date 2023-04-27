"""Module to with functions and utilities to calculate CAM on an image"""

from pathlib import Path

import numpy as np
import tensorflow as tf
from cv2 import cv2
from tensorflow.keras import Model  # pylint:disable= import-error
from tensorflow.keras.models import load_model  # pylint:disable= import-error
from tensorflow.keras.utils import (  # pylint:disable= import-error
    img_to_array,
    load_img,
)

from niceml.experiments.expdatalocalstorageloader import create_expdata_from_local_storage
from niceml.experiments.experimentdata import ExperimentData


# pylint:disable=c-extension-no-member
def run_cam_on_img(img_file: str, experiment_path: str):
    """
    1. Load image from file
    2. Load model from experiment output
    3. Extract Conv Layer from model
    4. Calc CAM
    5. Create Heatmap image
    6. Save image to experiment directory
    Args:
        experiment_path: path to experiment output
        img_file: original image path

    """

    exp: ExperimentData = create_expdata_from_local_storage(experiment_path)

    model = _load_model(exp)
    preprocessed_img = load_preprocessed_img(
        img_file=img_file, shape=model.input_shape[1:]
    )
    heatmap = create_heatmap(model=model, img=preprocessed_img, class_idx=0)
    cam_img = make_overlay(preprocessed_img, heatmap)

    output_image = cv2.addWeighted(
        cv2.cvtColor(preprocessed_img.astype("uint8"), cv2.COLOR_RGB2BGR),
        0.5,
        cam_img,
        1,
        0,
    )

    output_path = Path(experiment_path).joinpath(f"{Path(img_file).stem}_cam.png")
    cv2.imwrite(str(output_path), output_image)


def _load_model(exp: ExperimentData):
    """
    Load best model from experiment

    Args:
        exp: experiment (ExperimentData)

    Returns:
        tensorflow model
    """

    model = load_model(exp.get_model_path())
    return model


def load_preprocessed_img(img_file: str, shape: tuple):
    """

    Args:
        img_file: path to image file
        shape: input shape of model

    Returns:
        image as numpy array
    """

    img = load_img(img_file, target_size=shape)
    return img_to_array(img)


# pylint:disable = too-many-locals,c-extension-no-member
def create_heatmap(
    model: Model, img: np.ndarray, class_idx: int, layer_name: str = "conv"
) -> np.ndarray:
    """
    generates heatmap using last conv layer "conv" specified in create_model section

    Args:
        model: tensorflow Model
        img: image as numpy array
        class_idx: class index of output tensor
        layer_name: last conv layer name - DEFAULT: "conv"

    Returns:
        heatmap as numpy array
    """

    grad_model = Model(
        [model.input], [model.get_layer(name=layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(np.array([img]))
        loss = predictions[:, class_idx]

    output = conv_outputs[0]
    grads = tape.gradient(loss, conv_outputs)[0]

    tf.cast(output > 0, "float32")
    tf.cast(grads > 0, "float32")
    guided_grads = (
        tf.cast(output > 0, "float32") * tf.cast(grads > 0, "float32") * grads
    )

    weights = tf.reduce_mean(guided_grads, axis=(0, 1))

    cam = np.ones(output.shape[0:2], dtype=np.float32)

    for index, weight in enumerate(weights):
        cam += weight * output[:, :, index]

    cam = cv2.resize(cam.numpy(), (img.shape[0], img.shape[1]))
    cam = np.maximum(cam, 0)
    heatmap = (cam - cam.min()) // (cam.max() - cam.min())

    return heatmap


# pylint:disable=c-extension-no-member
def make_overlay(img: np.ndarray, heatmap: np.ndarray) -> np.ndarray:
    """
    generates a weighted image based on cam heatmap

    Args:
        img: original image as numpy array
        heatmap: heatmap as numpy array

    Returns:
        cam image as numpy array
    """

    cam = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
    return cv2.addWeighted(
        cv2.cvtColor(img.astype("uint8"), cv2.COLOR_RGB2BGR), 0.5, cam, 1, 0
    )
