"""Module for focal loss for semantic segmentation"""
import tensorflow as tf
from keras.backend import epsilon


class SemSegFocalLoss(tf.losses.Loss):  # pylint: disable=too-few-public-methods
    """Implements Focal loss"""

    def __init__(
        self,
        alpha: float = 0.25,
        gamma: float = 2.0,
        weight: float = 1.0,
        use_background_class: bool = False,
    ):
        """initialize SemSegFocalLoss parameters"""
        super().__init__(reduction="none", name="SemSegFocalLoss")
        self._alpha = alpha
        self._gamma = gamma
        self._weight = weight
        self.use_background_class = use_background_class

    def call(self, y_true, y_pred):
        """Calculate SemSegFocalLoss based on prediction and ground-truth array

        Args:
            y_true: np.ndarray with shape (batch_size x height x width x num_classes)
            y_pred: np.ndarray with shape (batch_size x height x width x num_classes)

        Returns:
            Focal loss
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

        # set all prediction values of void_class to 0
        if self.use_background_class:
            shape = tf.shape(y_true)
            zeros_tensor = tf.zeros(shape)
            y_true = tf.concat(
                [y_true[:, :, :, :-1], zeros_tensor[:, :, :, -1:]], axis=-1
            )

        alpha = tf.where(tf.equal(y_true, 1.0), self._alpha, (1.0 - self._alpha))
        loss = alpha * tf.pow(1.0 - targets, self._gamma) * binary_cross_entropy
        cls_loss = tf.reduce_sum(loss, axis=[1, 2, 3])
        cls_loss = tf.math.divide_no_nan(cls_loss, normalizer)
        return cls_loss * self._weight
