"""Module for NormalizationInfo"""
from attr import define


@define
class NormalizationInfo:
    """Class for normalization infos"""

    feature_key: str
    offset: float
    divisor: float
