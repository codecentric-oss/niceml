"""Module for PredictionFilterType"""

from enum import Enum


class PredictionFilterTypes(str, Enum):
    """Enum for the types of prediction filters."""

    THRESHOLD = "Threshold"
    NMS = "NMS"
    UNIFIED_BOX = "UnifiedBox"
