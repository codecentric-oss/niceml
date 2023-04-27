import numpy as np

from niceml.utilities.masks.maskdownscale import get_downscaled_masked_histogram


def test_maskdownscale():
    cur_size_x = 100
    cur_size_y = 120
    cur_array = np.zeros((cur_size_y, cur_size_x), dtype=int)
    default_value = 255
    cur_array[:, :] = default_value

    cur_array[0:10, 0:10] = 0
    cur_array[15:25, 15:25] = 1
    cur_array[40:60, 40:60] = 9
    ds_factor = 5
    num_classes = 10
    mask_hist = get_downscaled_masked_histogram(
        cur_array, num_classes, default_value, ds_factor
    )
    assert mask_hist.shape == (
        cur_size_y // ds_factor,
        cur_size_x // ds_factor,
        num_classes,
    )
    assert np.sum(mask_hist[:, :, 0]) == 100
    assert np.sum(mask_hist[:, :, 1]) == 100
    assert np.sum(mask_hist[:, :, 9]) == 400

    cur_array[40:60, 40:60] = 10
    try:
        get_downscaled_masked_histogram(
            cur_array, num_classes, default_value, ds_factor
        )
    except IndexError:
        assert True
