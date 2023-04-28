from typing import List, Union

import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as kb


@tf.keras.utils.register_keras_serializable()
class CategoricalFocalLoss(tf.keras.losses.Loss):
    def __init__(self, alpha: Union[float, List[float]], gamma: float = 2.0, **kwargs):
        """
        Inspired by https://github.com/umbertogriffo/focal-loss-keras
        Focal loss which can be applied to softmax outputs.
        Official paper: https://arxiv.org/pdf/1708.02002.pdf
        Parameters
        ----------
        alpha: float or list of float
            When float alpha is applied to all classes otherwise the list
            must have the same length as classes with each alpha applied
            to it's own class
        gamma: float
            gamma value of the paper
        kwargs:
            all parameters are applied to tensorflow loss
        """
        super().__init__(**kwargs)
        self.alpha = np.array(alpha, dtype=np.float32)
        self.gamma = gamma

    def __call__(self, y_true, y_pred, sample_weight=None):

        # Clip the prediction value to prevent NaN's and Inf's
        epsilon = kb.epsilon()
        y_pred = kb.clip(y_pred, epsilon, 1.0 - epsilon)
        # normal cross entropy calculation
        cross_entropy = -y_true * kb.log(y_pred)
        # reweight wrt focal loss paper
        loss = self.alpha * kb.pow(1 - y_pred, self.gamma) * cross_entropy

        return kb.mean(kb.sum(loss, axis=-1))
