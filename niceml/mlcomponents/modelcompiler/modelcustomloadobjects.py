"""Module for ModelCustomLoadObjects"""
from importlib import import_module

from pydantic import BaseModel, Field

from niceml.config.config import InitConfig, get_class_path


class ModelCustomLoadObjects(InitConfig):
    """Only used to import modules required for the model (e.g. tensorflow)"""

    objects: dict = Field(
        default_factory=dict,
        description="Dict of objects to import while loading the model",
    )

    def __call__(self) -> dict:
        ret_dict = dict()
        for key, value in self.objects.items():
            if type(value) is str:
                ret_dict[key] = import_module(value)
            else:
                ret_dict[key] = value
        return ret_dict
