"""Module for ModelCustomLoadObjects"""
import json
from importlib import import_module
from typing import Optional

from pydantic import BaseModel, Field

from niceml.config.config import InitConfig, get_class_path, Configurable


class ModelCustomLoadObjects(Configurable):
    """Only used to import modules required for the model (e.g. tensorflow)"""

    def __init__(self, objects: Optional[dict] = None):
        """
        Only used to import modules required for the model (e.g. tensorflow)
        Args:
            objects: Dict of objects to import while loading the model
        """

        self.objects = objects or {}

    def load(self) -> dict:
        ret_dict = dict()
        for key, value in self.objects.items():
            if type(value) is str:
                ret_dict[key] = import_module(value)
            else:
                ret_dict[key] = value
        return ret_dict
