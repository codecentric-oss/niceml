"""Module for AugmentationProcessor"""
from abc import ABC, abstractmethod
from typing import Any


class AugmentationProcessor(ABC):
    """Is used by the GenericDataset to augument the input containers"""

    @abstractmethod
    def __call__(self, input_container: Any) -> Any:
        """The augmentation processor is called to augment an input container"""
