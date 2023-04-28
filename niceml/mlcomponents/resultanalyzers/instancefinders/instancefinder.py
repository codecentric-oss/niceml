"""Module of the abstract InstanceFinder"""
from abc import ABC

from niceml.mlcomponents.resultanalyzers.tensors.tensormetric import TensorMetric


# pylint: disable = too-many-arguments, too-few-public-methods
class InstanceFinder(TensorMetric, ABC):
    """Abstract class of an instance finder that finds error instances in a mask."""

    def __init__(
        self,
        key: str,
        min_area: int,
        max_area: int,
        threshold: float,
    ):
        super().__init__(key=key)
        self.threshold = threshold
        self.max_area = max_area
        self.min_area = min_area
