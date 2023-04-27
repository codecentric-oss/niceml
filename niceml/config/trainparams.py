"""module for trainparams"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class TrainParams:
    """TrainParams are used to select the amount of steps and epochs for training"""

    epochs: int
    steps_per_epoch: Optional[int] = None
    validation_steps: Optional[int] = None
