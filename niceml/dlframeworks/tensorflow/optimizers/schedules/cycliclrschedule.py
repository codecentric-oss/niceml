"""Module for cycliclearningrateschedule"""
from typing import Optional

import tensorflow as tf

# pylint: disable=import-error, no-name-in-module
from tensorflow.keras.optimizers.schedules import LearningRateSchedule


class CyclicLRSchedule(LearningRateSchedule):
    """Cyclic learning rate schedule"""

    def __init__(self, max_lr: float, cycle_size: int, min_lr: Optional[float] = None):
        super().__init__()
        self.max_lr = max_lr
        self.cycle_size = cycle_size
        self.min_lr = min_lr or max_lr / 10

    def __call__(self, step):
        """Return the learning rate for a given step"""
        step = tf.cast(step, tf.float32)
        cycle = tf.floor(1 + step / self.cycle_size)
        x_value = tf.abs(step / (self.cycle_size / 2) - 2 * cycle + 1)
        learning_rate = self.min_lr + (self.max_lr - self.min_lr) * tf.maximum(
            0.0, (1 - x_value)
        )
        return learning_rate

    def get_config(self) -> dict:
        """Return the config of the schedule"""
        return {
            "max_lr": self.max_lr,
            "cycle_size": self.cycle_size,
            "min_lr": self.min_lr,
        }
