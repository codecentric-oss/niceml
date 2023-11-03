"""Abstract class for prediction functions"""
from abc import ABC, abstractmethod
from typing import Any


class PredictionFunction(ABC):
    """Abstract class for prediction functions"""

    @abstractmethod
    def predict(self, model, data_x) -> Any:
        """Predicts the given data with the given model"""
        raise NotImplementedError
