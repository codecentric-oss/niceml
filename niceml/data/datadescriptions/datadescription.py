"""Module for abstract DataDescription"""
from abc import ABC

from dagster import Config


class DataDescription(ABC, Config):  # pylint: disable=too-few-public-methods
    """This class is used to define the format of the input and target data.
    E.g. how big the input image size is, or what target classes are used."""
