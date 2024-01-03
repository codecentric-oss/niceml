"""module for trainparams"""
from typing import Optional

from pydantic import Field

from niceml.config.config import Config


class TrainParams(Config):
    """TrainParams are used to select the amount of steps and epochs for training"""

    epochs: int = Field(description="Number of trainings epochs.", default=1)
    steps_per_epoch: Optional[int] = Field(
        description="Number of batches to process in a training epoch.", default=None
    )
    validation_steps: Optional[int] = Field(
        description="Number of validation steps between two epochs.", default=None
    )
