"""Module for object detection metrics for integration into model training"""

import tensorflow as tf

from niceml.utilities.boundingboxes.boundingbox import (
    IGNORE_MASK_VALUE,
    NEGATIVE_MASK_VALUE,
    POSITIVE_MASK_VALUE,
)


class AvgPosPredObjDet:  # pylint: disable=too-few-public-methods
    """Positive Classification Values for object detection"""

    def __init__(self, name: str = "avg_pos_pred"):

        self.__name__ = name

    def __call__(self, y_true, y_pred):
        y_pred = tf.cast(y_pred, dtype=tf.float32)

        cls_predictions = y_pred[:, :, 4:]
        cls_labels = y_true[:, :, 5:]

        probs = tf.nn.sigmoid(cls_predictions)
        probs = tf.where(tf.equal(cls_labels, 1.0), probs, 0.0)
        probs = tf.reduce_sum(probs, axis=[-1, -2])
        avg_probs = tf.math.divide_no_nan(
            probs, tf.reduce_sum(cls_labels, axis=[-1, -2])
        )
        return avg_probs


class AvgNegPredObjDet:  # pylint: disable=too-few-public-methods
    """Negative Classification Values for object detection"""

    def __init__(self, name: str = "avg_neg_pred"):

        self.__name__ = name

    def __call__(self, y_true, y_pred):
        y_pred = tf.cast(y_pred, dtype=tf.float32)

        cls_predictions = y_pred[:, :, 4:]
        cls_labels = y_true[:, :, 5:]
        ignore_mask = tf.cast(
            tf.equal(y_true[:, :, 4], IGNORE_MASK_VALUE), dtype=tf.float32
        )
        not_ignore_mask = tf.cast(
            tf.expand_dims(tf.equal(ignore_mask, 0.0), axis=2), dtype=tf.float32
        )

        probs = tf.nn.sigmoid(cls_predictions)
        negative_count_mask = tf.cast(
            tf.logical_and(tf.equal(cls_labels, 0.0), tf.equal(not_ignore_mask, 1.0)),
            dtype=tf.float32,
        )
        probs = tf.where(tf.equal(negative_count_mask, 1.0), probs, 0.0)
        probs = tf.reduce_sum(probs, axis=[-1, -2])
        avg_probs = tf.math.divide_no_nan(
            probs, tf.reduce_sum(negative_count_mask, axis=[-1, -2])
        )
        return avg_probs


class AvgPosTargetCountObjDet:  # pylint: disable=too-few-public-methods
    """Average positive target count for one image in object detection"""

    def __init__(self, name: str = "avg_pos_target_count"):
        self.__name__ = name

    def __call__(self, y_true, y_pred):
        positive_mask = tf.cast(
            tf.equal(y_true[:, :, 4], POSITIVE_MASK_VALUE), dtype=tf.float32
        )
        positive_mask_count = tf.reduce_sum(positive_mask, axis=-1)

        return positive_mask_count


class AvgNegTargetCountObjDet:  # pylint: disable=too-few-public-methods
    """Average negative target count for one image in object detection"""

    def __init__(self, name: str = "avg_neg_target_count"):
        self.__name__ = name

    def __call__(self, y_true, y_pred):
        negative_mask = tf.cast(
            tf.equal(y_true[:, :, 4], NEGATIVE_MASK_VALUE), dtype=tf.float32
        )
        negative_mask_count = tf.reduce_sum(negative_mask, axis=-1)

        return negative_mask_count
