import pytest
import tensorflow as tf

from niceml.dlframeworks.tensorflow.metrics.semsegmetrics import (
    AvgNegPredSemSeg,
    AvgNegTargetCountSemSeg,
    AvgPosPredSemSeg,
    AvgPosTargetCountSemSeg,
)


@pytest.fixture()
def y_true():
    return tf.constant(
        [
            [
                [[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                [[0, 1, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]],
                [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
            ],
            [
                [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0]],
                [[0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]],
                [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0]],
            ],
        ],
        dtype=tf.float32,
    )


@pytest.fixture()
def y_pred():
    return tf.constant(
        [
            [
                [
                    [0.1, 0.9, 0.2, 0.5],
                    [0.3, 0.2, 0.7, 0.1],
                    [0.4, 0.3, 0.3, 0.8],
                ],
                [
                    [0.5, 0.4, 0.3, 0.9],
                    [0.9, 0.1, 0.1, 0.1],
                    [0.2, 0.7, 0.1, 0.1],
                ],
                [
                    [0.8, 0.1, 0.1, 0.2],
                    [0.2, 0.7, 0.1, 0.1],
                    [0.3, 0.3, 0.4, 0.7],
                ],
            ],
            [
                [
                    [0.6, 0.1, 0.1, 0.3],
                    [0.2, 0.3, 0.7, 0.2],
                    [0.1, 0.7, 0.2, 0.4],
                ],
                [
                    [0.3, 0.4, 0.7, 0.3],
                    [0.3, 0.7, 0.1, 0.2],
                    [0.9, 0.1, 0.1, 0.2],
                ],
                [
                    [0.2, 0.7, 0.1, 0.3],
                    [0.9, 0.1, 0.1, 0.2],
                    [0.3, 0.3, 0.4, 0.7],
                ],
            ],
        ],
        dtype=tf.float32,
    )


def test_avgpospredsemseg(y_true, y_pred):
    avg_pos_pred = AvgPosPredSemSeg()

    result = avg_pos_pred(y_true, y_pred)
    expected = tf.constant([0.70000005, 0.7])
    assert tf.experimental.numpy.allclose(result, expected)


def test_avgnegpredsemseg(y_true, y_pred):
    avg_neg_pred = AvgNegPredSemSeg()
    result = avg_neg_pred(y_true, y_pred)
    expected = tf.constant([0.25555557, 0.22962964])
    assert tf.experimental.numpy.allclose(result, expected)


def test_avgpostargetcountsemseg(y_true, y_pred):
    avgpostargetcountsemseg = AvgPosTargetCountSemSeg()
    result = avgpostargetcountsemseg(y_true, y_pred)

    expected = tf.constant([8.0, 9.0])
    assert tf.reduce_all(tf.equal(result, expected))


def test_avgnegtargetcountsemseg(y_true, y_pred):
    avgnegtargetcountsemseg = AvgNegTargetCountSemSeg()
    result = avgnegtargetcountsemseg(y_true, y_pred)

    expected = tf.constant([1.0, 0.0])
    assert tf.reduce_all(tf.equal(result, expected))
