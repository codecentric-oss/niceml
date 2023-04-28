"""Module for abstract DataDescription"""
from abc import ABC


class DataDescription(ABC):  # pylint: disable=too-few-public-methods
    """This class is used to describe the data. E.g. how big the input image size is,
    or what target classes are used."""
