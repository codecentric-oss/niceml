"""Module to wrap cython maskdownscale"""
import numpy as np
import pyximport

pyximport.install(setup_args={"include_dirs": np.get_include()})
from niceml.utilities.masks.cymaskdownscale import (  # pylint: disable=no-name-in-module,wrong-import-position,import-error
    cy_mask_downscale,
)


def get_downscaled_masked_histogram(
    mask_image: np.ndarray, num_classes: int, default_value: int, ds_factor: int
) -> np.ndarray:
    """
    Calculates a simple histogram for the downscaled mask image
    Args:
        mask_image: image to downscale
        num_classes: number of classes included in image
        default_value: background value of the image
        ds_factor: downscale factor

    Returns:
        Masked histogram
    """
    img_shape = mask_image.shape
    hist_shape = (
        int(img_shape[0] // ds_factor),
        int(img_shape[1] // ds_factor),
        num_classes,
    )
    mask_hist = np.zeros(hist_shape, int)
    mask_image = mask_image.astype(np.uint8)
    try:
        mask_hist = cy_mask_downscale(mask_image, mask_hist, default_value, ds_factor)
    except IndexError as excep:
        max_mask_img = np.max(mask_image[mask_image != default_value])
        raise IndexError(
            f"MaskImage contains {max_mask_img} but "
            f"highest allowed value is: {num_classes - 1}"
        ) from excep
    return mask_hist
