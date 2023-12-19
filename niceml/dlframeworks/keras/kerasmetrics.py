"""Module for metrics in keras"""
import tensorflow as tf
from tensorflow import logical_and, logical_or, reduce_mean, reduce_sum
from tensorflow import round as tf_round
from tensorflow.python.ops.math_ops import div_no_nan


class MeanIoU:  # pylint: disable=too-few-public-methods
    """Keras Metric for Mean IoU"""

    def __init__(self, name: str = "mean_iou"):
        self.__name__ = name

    def __call__(self, y_true, y_pred):
        y_true_round = tf.cast(tf_round(y_true), tf.bool)
        y_pred_round = tf.cast(tf_round(y_pred), tf.bool)
        intersect = tf.cast(logical_and(y_pred_round, y_true_round), tf.float32)
        union = tf.cast(logical_or(y_pred_round, y_true_round), tf.float32)

        union_sum = reduce_sum(union, axis=-1)
        intersect_sum = reduce_sum(intersect, axis=-1)
        ious = div_no_nan(intersect_sum, union_sum)

        mean_iou = reduce_mean(ious)
        return mean_iou
