from typing import List, Tuple

import pytest
import tensorflow as tf

from niceml.dlframeworks.tensorflow.losses.semseglosses import SemSegFocalLoss


@pytest.fixture()
def tensor_shape() -> Tuple:
    tensor_shape = (2, 4, 4, 3)
    return tensor_shape


@pytest.mark.parametrize(
    "alpha,gamma,min_expected_vals",
    [(0.25, 10.0, [4.2, 4.2]), (0.99, 2.0, [17.0, 17.0]), (0.25, 2.0, [4.3, 4.3])],
)
def test_positive_zero_preds(
    alpha: float, gamma: float, min_expected_vals: List[float], tensor_shape: Tuple
):

    preds = tf.ones(tensor_shape) * 0.003
    gts = tf.ones(tensor_shape)

    loss = SemSegFocalLoss(alpha=alpha, gamma=gamma)

    loss_val = loss(gts, preds)

    min_expected = tf.constant(min_expected_vals, dtype=tf.float32)

    assert all(tf.greater_equal(loss_val, min_expected))


@pytest.mark.parametrize(
    "alpha,gamma,max_expected_vals",
    [
        (0.25, 10.0, [1e-25, 1e-25]),
        (0.99, 2.0, [1e-7, 1e-7]),
        (0.25, 2.0, [1e-7, 1e-7]),
    ],
)
def test_positive_one_preds(
    alpha: float, gamma: float, max_expected_vals: List[float], tensor_shape: Tuple
):

    preds = tf.ones(tensor_shape) * 0.997
    gts = tf.ones(tensor_shape)

    loss = SemSegFocalLoss(alpha=alpha, gamma=gamma)

    loss_val = loss(gts, preds)

    max_expected = tf.constant(max_expected_vals, dtype=tf.float32)

    assert all(tf.greater_equal(max_expected, loss_val))


@pytest.mark.parametrize(
    "alpha,gamma,max_expected_vals",
    [
        (0.25, 10.0, [1e-25, 1e-25]),
        (0.99, 2.0, [1e-7, 1e-7]),
        (0.25, 2.0, [1e-7, 1e-7]),
    ],
)
def test_negative_zero_preds(
    alpha: float, gamma: float, max_expected_vals: List[float], tensor_shape: Tuple
):
    preds = tf.ones(tensor_shape) * 0.003
    gts = tf.zeros(tensor_shape)

    loss = SemSegFocalLoss(alpha=alpha, gamma=gamma)

    loss_val = loss(gts, preds)

    max_expected = tf.constant(max_expected_vals, dtype=tf.float32)

    assert all(tf.greater_equal(max_expected, loss_val))


@pytest.mark.parametrize(
    "alpha,gamma,min_expected_vals",
    [(0.99, 2.0, [0.17, 0.17]), (0.25, 10.0, [12.0, 12.0]), (0.25, 2.0, [12.0, 12.0])],
)
def test_negative_one_preds(
    alpha: float, gamma: float, min_expected_vals: List[float], tensor_shape: Tuple
):
    preds = tf.ones(tensor_shape) * 0.997
    gts = tf.zeros(tensor_shape)

    loss = SemSegFocalLoss(alpha=alpha, gamma=gamma)

    loss_val = loss(gts, preds)

    min_expected = tf.constant(min_expected_vals, dtype=tf.float32)

    assert all(tf.greater_equal(loss_val, min_expected))
