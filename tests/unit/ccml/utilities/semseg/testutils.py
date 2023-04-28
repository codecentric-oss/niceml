from typing import List, Tuple

import numpy as np


def get_random_semseg_mask(
    image_shape: Tuple[int, int],
    random_generator: np.random.Generator,
    class_list: List[str],
    square_width: int,
    square_height: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates random mask with random squares representing errors on an image
    Args:
        square_width: width of the squares
        square_height: height of the squares
        image_shape: Shape of the image
        random_generator: Seeded generator to create random image
        class_list: Classes that are used to create the squares

    Returns:
        Returns a numpy array of the shape (height x width) with the value
        0 (background) or the index of a class at each position.
        Also returns a numpy array of the same shape with a value
        between 0.0 and 1.0 at each position where there is no 0 in the first array,
        otherwise it is 0

    """
    index_image = np.zeros(shape=image_shape)

    for class_idx in class_list:
        center_y = random_generator.integers(
            low=int(square_height / 2), high=image_shape[0] - int(square_height / 2)
        )
        center_x = random_generator.integers(
            low=int(square_width / 2), high=image_shape[1] - int(square_width / 2)
        )

        index_image[
            center_y - int(square_height / 2) : center_y + int(square_height / 2),
            center_x - int(square_width / 2) : center_x + int(square_width / 2),
        ] = float(class_idx)

    binary_index_image = np.where(index_image == 0, index_image, 1)
    pred_image = random_generator.uniform(low=0.5, high=1.0, size=image_shape)
    pred_image = binary_index_image * pred_image

    return index_image, pred_image


def get_result_mask(
    coords: List[Tuple[int, int]], image_shape: Tuple[int, int]
) -> np.ndarray:
    """
    Creates a binary mask based on given coords.
    Args:
        coords: Coords set to 1
        image_shape: Shape of the image

    Returns:
        Binary mask (0,255) as numpy array

    """
    mask = np.zeros(shape=image_shape)

    for coord in coords:
        mask[coord[0], coord[1]] = 255.0
    return mask
