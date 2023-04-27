"""Module for ModelCustomLoadObjects"""
from dataclasses import dataclass, field
from importlib import import_module


@dataclass
class ModelCustomLoadObjects:
    """Only used to import modules required for the model (e.g. tensorflow)"""

    objects: dict = field(default_factory=dict)

    def __call__(self) -> dict:
        ret_dict = dict()
        for key, value in self.objects.items():
            if type(value) is str:
                ret_dict[key] = import_module(value)
            else:
                ret_dict[key] = value
        return ret_dict
