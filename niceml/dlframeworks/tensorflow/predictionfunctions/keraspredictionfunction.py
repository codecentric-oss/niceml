"""module for keras prediction function"""
from typing import Any

from niceml.mlcomponents.predictionfunction.predictionfunction import PredictionFunction


class KerasPredictionFunction(PredictionFunction):
    """Prediction function for keras models"""

    def predict(self, model, data_x) -> Any:
        pred = model.predict_step(data_x).numpy()
        return pred
