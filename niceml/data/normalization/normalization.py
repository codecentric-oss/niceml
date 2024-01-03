"""Module for NormalizationInfo"""
from attr import define, dataclass


@dataclass
class NormalizationInfo:
    """Class for normalization infos"""

    feature_key: str


@dataclass
class ScalarNormalizationInfo(NormalizationInfo):
    """Class for scalar normalization infos"""

    offset: float
    divisor: float


@dataclass
class BinaryNormalizationInfo(NormalizationInfo):
    """Class for binary normalization infos"""

    values: list


@dataclass
class CategoricalNormalizationInfo(NormalizationInfo):
    """Class for categorical normalization infos"""

    values: list
