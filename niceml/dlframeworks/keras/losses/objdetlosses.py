"""losses for object detection"""
from typing import List, Optional

import tensorflow as tf

from niceml.utilities.boundingboxes.boundingbox import (
    IGNORE_MASK_VALUE,
    POSITIVE_MASK_VALUE,
)


class RetinaNetBoxLoss(tf.losses.Loss):  # pylint: disable=too-few-public-methods
    """Implements Smooth L1 loss"""

    def __init__(self, delta: float = 1.0):
        super().__init__(reduction="none", name="RetinaNetBoxLoss")
        self._delta = delta

    def call(self, y_true, y_pred):
        """
        Parameters
        ----------
        y_true: np.ndarray with shape (count_anchors x 4+1 + num_classes)
        y_pred: np.ndarray with shape (count_anchors x 4 + num_classes)
        """
        positive_mask = tf.cast(
            tf.equal(y_true[:, :, 4], POSITIVE_MASK_VALUE), dtype=tf.float32
        )
        normalizer = tf.reduce_sum(positive_mask, axis=-1)

        y_pred = tf.cast(y_pred, dtype=tf.float32)

        box_labels = y_true[:, :, :4]
        box_predictions = y_pred[:, :, :4]

        difference = box_labels - box_predictions
        absolute_difference = tf.abs(difference)
        squared_difference = difference**2
        loss = tf.where(
            tf.less(absolute_difference, self._delta),
            0.5 * squared_difference,
            absolute_difference - 0.5,
        )

        box_loss = tf.reduce_sum(loss, axis=-1)

        box_loss = tf.where(tf.equal(positive_mask, 1.0), box_loss, 0.0)
        box_loss = tf.math.divide_no_nan(tf.reduce_sum(box_loss, axis=-1), normalizer)

        return box_loss


class RetinaNetClsLoss(tf.losses.Loss):  # pylint: disable=too-few-public-methods
    """Implements Focal loss"""

    def __init__(self, alpha: float = 0.25, gamma: float = 2.0):
        super().__init__(reduction="none", name="RetinaNetClsLoss")
        self._alpha = alpha
        self._gamma = gamma

    def call(self, y_true, y_pred):
        """
        Parameters
        ----------
        y_true: np.ndarray with shape (count_anchors x 4+1 + num_classes)
        y_pred: np.ndarray with shape (count_anchors x 4 + num_classes)
        """

        ignore_mask = tf.cast(
            tf.equal(y_true[:, :, 4], IGNORE_MASK_VALUE), dtype=tf.float32
        )
        not_ignore_mask = tf.cast(tf.equal(ignore_mask, 0.0), dtype=tf.float32)
        normalizer = tf.reduce_sum(not_ignore_mask, axis=-1)

        y_pred = tf.cast(y_pred, dtype=tf.float32)
        cls_labels = y_true[:, :, 5:]
        cls_predictions = y_pred[:, :, 4:]
        cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(
            labels=cls_labels, logits=cls_predictions
        )
        probs = tf.nn.sigmoid(cls_predictions)
        alpha = tf.where(tf.equal(cls_labels, 1.0), self._alpha, (1.0 - self._alpha))
        targets = tf.where(tf.equal(cls_labels, 1.0), probs, 1 - probs)
        loss = alpha * tf.pow(1.0 - targets, self._gamma) * cross_entropy
        cls_loss = tf.reduce_sum(loss, axis=-1)
        cls_loss = tf.where(tf.equal(ignore_mask, 1.0), 0.0, cls_loss)
        cls_loss = tf.math.divide_no_nan(tf.reduce_sum(cls_loss, axis=-1), normalizer)
        return cls_loss


class CombinationLoss(tf.losses.Loss):  # pylint: disable=too-few-public-methods
    """Wrapper to combine both the losses"""

    def __init__(self, losses: list, weights: Optional[List[float]] = None):
        super().__init__(reduction="auto", name="CombinationLoss")
        self.weights = weights or [1.0] * len(losses)
        self.losses = losses

        if len(self.weights) != len(self.losses):
            raise ValueError(
                f"Length of self.weights ({len(self.weights)}) is not "
                f"equal the length of self.losses ({self.losses})"
            )

    def call(self, y_true, y_pred):
        """Calls sum of losses"""
        return sum(
            cur_loss(y_true, y_pred) * cur_weight
            for cur_loss, cur_weight in zip(self.losses, self.weights)
        )
