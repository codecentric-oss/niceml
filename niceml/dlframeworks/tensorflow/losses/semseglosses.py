"""Module for focal loss for semantic segementation"""

import tensorflow as tf
from keras.backend import epsilon


class SemSegFocalLoss(tf.losses.Loss):  # pylint: disable=too-few-public-methods
    """Implements Focal loss"""

    def __init__(self, alpha: float = 0.25, gamma: float = 2.0, weight: float = 1.0):
        super().__init__(reduction="none", name="SemSegFocalLoss")
        self._alpha = alpha
        self._gamma = gamma
        self._weight = weight

    def call(self, y_true, y_pred):
        """
        Parameters
        ----------
        y_true: np.ndarray with shape (batch_size x height x width x num_classes)
        y_pred: np.ndarray with shape (batch_size x height x width x num_classes)
        """
        normalizer = tf.cast(
            tf.shape(y_true, out_type=tf.int32)[1]
            * tf.shape(y_true, out_type=tf.int32)[2],
            dtype=tf.float32,
        )

        y_pred = tf.cast(y_pred, dtype=tf.float32)
        # pylint: disable = invalid-unary-operand-type
        targets = tf.where(tf.equal(y_true, 1.0), y_pred, (1.0 - y_pred))

        binary_cross_entropy = -tf.math.log(targets + epsilon())

        alpha = tf.where(tf.equal(y_true, 1.0), self._alpha, (1.0 - self._alpha))
        loss = alpha * tf.pow(1.0 - targets, self._gamma) * binary_cross_entropy
        cls_loss = tf.reduce_sum(loss, axis=[1, 2, 3])
        cls_loss = tf.math.divide_no_nan(cls_loss, normalizer)
        return cls_loss * self._weight
