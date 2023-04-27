from math import isclose
from typing import Tuple

import numpy as np
import pytest

from niceml.utilities.semseg.semseginstancelabeling import SemSegInstanceLabel
from tests.unit.ccml.utilities.semseg.testutils import get_random_semseg_mask


@pytest.mark.parametrize(
    " result_iou,image_shape,square_width,square_height,class_label,class_index, seed",
    [
        (1.0, (10, 10), 4, 4, "1", 1, 40),
        (0.0, (10, 10), 2, 2, "1", 1, 42),
        (0.23076923076923078, (20, 20), 8, 8, "1", 1, 22),
    ],
)
def test_semseg_iou(
    result_iou: float,
    image_shape: Tuple[int, int],
    square_width: int,
    square_height: int,
    class_label: str,
    class_index: int,
    seed: int,
):  # pylint: disable =too-many-arguments

    random_generator = np.random.default_rng(seed=seed)

    semseg_label_mask, _ = get_random_semseg_mask(
        image_shape=image_shape,
        random_generator=random_generator,
        class_list=[str(class_index)],
        square_width=square_width,
        square_height=square_height,
    )
    other_mask, _ = get_random_semseg_mask(
        image_shape=image_shape,
        random_generator=random_generator,
        class_list=[str(class_index)],
        square_width=square_width,
        square_height=square_height,
    )

    semseg_label = SemSegInstanceLabel(
        mask=semseg_label_mask, class_name=class_label, class_index=class_index
    )
    other = SemSegInstanceLabel(
        mask=other_mask, class_name=class_label, class_index=class_index
    )
    iou = semseg_label.calc_iou(other=other)

    assert isclose(iou, result_iou)
