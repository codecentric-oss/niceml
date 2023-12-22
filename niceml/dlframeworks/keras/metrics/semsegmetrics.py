"""Module for metrics for semantic segmentation """
import tensorflow as tf


class AvgPosPredSemSeg:  # pylint: disable=too-few-public-methods
    """Positive Classification Values for semantic segmentation"""

    def __init__(self, name: str = "avg_pos_pred"):
        self.__name__ = name

    def __call__(self, y_true, y_pred):
        pos_mask = tf.cast(tf.math.equal(y_true, 1.0), dtype=tf.float32)
        return avg_mask_prediction_value(pos_mask, y_pred)


class AvgNegPredSemSeg:  # pylint: disable=too-few-public-methods
    """Negative Classification Values for semantic segmentation"""

    def __init__(self, name: str = "avg_neg_pred"):
        self.__name__ = name

    def __call__(self, y_true, y_pred):
        neg_mask = tf.cast(tf.math.equal(y_true, 0.0), dtype=tf.float32)
        return avg_mask_prediction_value(neg_mask, y_pred)


def avg_mask_prediction_value(mask, prediction):
    """Average prediction value for a given mask"""
    prob_values = tf.where(tf.equal(mask, 1.0), prediction, 0.0)
    probs = tf.reduce_sum(prob_values, axis=[-1, -2, -3])
    mask_count = tf.reduce_sum(mask, axis=[-1, -2, -3])
    avg_probs = tf.math.divide_no_nan(probs, mask_count)
    return avg_probs


class AvgPosTargetCountSemSeg:  # pylint: disable=too-few-public-methods
    """Average positive target count for one image in semantic segmentation"""

    def __init__(self, name: str = "avg_pos_target_count"):
        self.__name__ = name

    def __call__(self, y_true, y_pred):
        pos_mask = tf.reduce_sum(y_true, axis=-1)
        pos_mask = tf.cast(tf.math.greater_equal(pos_mask, 1.0), dtype=tf.float32)
        pos_count = tf.reduce_sum(pos_mask, axis=[-1, -2])
        return pos_count


class AvgNegTargetCountSemSeg:  # pylint: disable=too-few-public-methods
    """Average negative target count for one image in semantic segmentation"""

    def __init__(self, name: str = "avg_neg_target_count"):
        self.__name__ = name

    def __call__(self, y_true, y_pred):
        neg_mask = tf.reduce_sum(y_true, axis=-1)
        neg_mask = tf.cast(tf.math.equal(neg_mask, 0.0), dtype=tf.float32)
        neg_count = tf.reduce_sum(neg_mask, axis=[-1, -2])
        return neg_count
