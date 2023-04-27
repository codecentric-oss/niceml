"""Module to use cython for transform mask images"""
import numpy as np
import pyximport

pyximport.install(setup_args={"include_dirs": np.get_include()})
from niceml.data.dataloaders.semseg.cytransformmaskimage import (
    transform_mask_image as cy_transform_mask_image,
)


def transform_mask_image(
    input_mask_image: np.ndarray, color_idx_lut: np.ndarray
) -> np.ndarray:
    """Fast implementation with cython to load labels faster"""
    if len(input_mask_image.shape) == 2:
        input_mask_image = input_mask_image[:, :, np.newaxis]
    if len(color_idx_lut.shape) == 1:
        color_idx_lut = color_idx_lut[:, np.newaxis]
    input_shape = input_mask_image.shape
    out_mask_array = np.ones((input_shape[0], input_shape[1]), dtype=int) * 255
    return cy_transform_mask_image(input_mask_image, color_idx_lut, out_mask_array)
