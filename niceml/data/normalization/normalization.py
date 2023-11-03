"""Module for NormalizationInfo"""
from attr import define


@define
class NormalizationInfo:
    """Class for normalization infos"""

    feature_key: str


@define
class ScalarNormalizationInfo(NormalizationInfo):
    """Class for scalar normalization infos"""

    offset: float
    divisor: float


@define
class BinaryNormalizationInfo(NormalizationInfo):
    """Class for binary normalization infos"""

    values: list


@define
class CategoricalNormalizationInfo(NormalizationInfo):
    """Class for categorical normalization infos"""

    values: list
