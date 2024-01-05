"""Module providing configuration-related functionality.

This module defines classes and functions for working with configurations in the context of the Dagster framework
and niceML's Hydra integration.
"""
from __future__ import annotations

import inspect
from abc import ABC
from enum import Enum
from inspect import isabstract
from typing import Optional, get_type_hints, Any, Tuple, Dict, List

from dagster import Config as DagsterConfig
from hydra.utils import instantiate, ConvertMode
from pydantic import Field, create_model


class Config(DagsterConfig, ABC):  # TODO: remove class
    """Base configuration class for Dagster and NiceML.

    This class inherits from DagsterConfig and ABC, providing a foundation for creating configuration instances.
    """

    @classmethod
    def create(cls, **kwargs) -> "Config":
        """Create a Config instance with parsed values. The parsed values could be a `BaseModel`, an `InitConfig`
        or default python datatypes.

        Args:
            **kwargs: Key-value pairs representing configuration parameters.

        Returns:
            An instance of the Config class with parsed values.
        """
        parsed_values = {key: parse_value(value) for key, value in kwargs.items()}

        return cls(**parsed_values)


class InitConfig(DagsterConfig):
    target: str = Field(
        ..., description="Target class which is instantiated.", alias="_target_"
    )

    def instantiate(self):
        return instantiate(self.dict(by_alias=True), _convert_=ConvertMode.ALL)

    @classmethod
    def create(cls, target_class, **kwargs):
        """Creates an instance of a pydantic BaseModel which have the same fields as given in kwargs"""
        conf_class = cls.create_conf_from_class(target_class)
        return conf_class(**kwargs)

    @classmethod
    def create_conf_from_class(cls, target_class):
        if issubclass(target_class, (InitConfig, DagsterConfig)):
            return target_class

        sig = inspect.signature(target_class.__init__)
        type_hints = get_type_hints(target_class.__init__)
        params = sig.parameters
        target_kwargs = {}
        if issubclass(target_class, Enum):
            target_enum_type = str if issubclass(target_class, str) else int
            target_kwargs["value"] = (target_enum_type, ...)
        for name, param in params.items():
            if name in ["self", "args", "kwargs"]:
                continue
            current_type = type_hints.get(name, Any)
            current_type = parse_value_type(param, cls)
            if param.default is not inspect._empty:
                target_kwargs[name] = (current_type, param.default)
            else:
                target_kwargs[name] = (current_type, ...)

        conf_class = create_model(
            f"Conf{target_class.__name__}",
            target=(str, Field(default=get_class_path(target_class), alias="_target_")),
            **target_kwargs,
            __base__=cls,
        )
        return conf_class

    @staticmethod
    def create_target_field(
        target_class,
        description: Optional[str] = None,
        default_value: Optional[dict] = None,
        example_value: Optional[dict] = None,
        **kwargs,
    ):
        """
        Used to configure Dagster Ops with a target class

        Args:
            target_class: class which is instantiated from the op
            description: description of the class or field
            default_value: default value of the field when nothing is provided
            **kwargs: additional kwargs passed to the Field class
        """
        if description is None:
            description = target_class.__doc__
        if default_value is None:
            impl_str: str = "implementation_of_" if isabstract(target_class) else ""
            default_value = f"{impl_str}{get_class_path(target_class)}"

        return Field(
            description=description,
            default=default_value,
            example_value=example_value,
            alias="_target_",
            **kwargs,
        )

    @staticmethod
    def create_config_field(
        target_class,
        description: Optional[str] = None,
        **kwargs,
    ):
        """
        Used to configure Dagster Ops with a InitConfig

        Args:
            target_class: class which is instantiated from the op
            **kwargs: additional kwargs passed to the Field class
        """
        if description is None:
            description = f"Implementation of class: {target_class.__name__} {target_class.__doc__}"

        return Field(
            description=description,
            **kwargs,
        )


def create_init_config(instance) -> InitConfig:
    """Create an InitConfig instance based on the provided instance's variables.

    Args:
        instance: An object with variables to be used in creating the InitConfig.

    Returns:
        An instance of the InitConfig class.
    """
    try:
        values = vars(instance)
        attributes = inspect.getmembers(
            instance,
            lambda attribute: not (inspect.isroutine(attribute)),
        )
        values = {}
        for attribute in attributes:
            key = attribute[0]
            value = attribute[1]
            if not key.startswith("_") and key != "Config":
                values[key] = value

    except TypeError:
        raise TypeError(type(instance))
    if isinstance(instance, Enum):
        return InitConfig.create(target_class=type(instance), value=instance.value)()
    parsed_values = {key: parse_value(value) for key, value in values.items()}
    return InitConfig.create(target_class=type(instance), **parsed_values)()


def parse_value(value):
    """Recursively parse a value, handling various types and creating InitConfig instances as needed.
    The value could be a `BaseModel`, an `InitConfig` or a default python datatype.
    Args:
        value: The value to be parsed.

    Returns:
        The parsed value.
    """
    if isinstance(value, Enum):
        return create_init_config(value)
    elif isinstance(value, (int, str, float, bool, InitConfig)) or value is None:
        return value
    elif isinstance(value, (list, tuple)):
        return [parse_value(item) for item in value]
    elif isinstance(value, dict):
        return {key: parse_value(value) for key, value in value.items()}
    else:
        return create_init_config(value)


def parse_value_type(value, cls):
    if isinstance(value, Enum):
        return create_model(
            f"Conf{value.__name__}",
            target=(str, Field(default=get_class_path(value), alias="_target_")),
            __base__=cls,
        )
    elif isinstance(value, (int, str, float, bool)):
        return type(value)
    elif isinstance(value, (int, str, float, bool, InitConfig)) or value is None:
        return type(value)
    elif isinstance(value, (list, tuple)):
        return [parse_value_type(item, cls) for item in value]
    elif isinstance(value, dict):
        return {key: parse_value_type(value, cls) for key, value in value.items()}
    else:
        return create_model(
            f"Conf{value.__name__}",
            target=(str, Field(default=get_class_path(value), alias="_target_")),
            __base__=cls,
        )


def get_class_path(cls):
    """Get the path of a class"""
    return f"{cls.__module__}.{cls.__name__}"


class MapInitConfig(DagsterConfig):
    """Hydra Map Config"""

    def instantiate(self):
        return instantiate(self.dict(by_alias=True), _convert_=ConvertMode.ALL)

    @staticmethod
    def create_config_field(
        target_class,
        description: Optional[str] = None,
        **kwargs,
    ):
        """
        Used to configure Dagster Ops with a MapInitConfig

        Args:
            target_class: class which is instantiated from the op
            **kwargs: additional kwargs passed to the Field class
        """
        if description is None:
            description = (
                f"Requires a map (Dict[str,{target_class.__name__}] "
                + target_class.__doc__
            )

        return Field(
            description=description,
            **kwargs,
        )


class Configurable(ABC):
    @classmethod
    def create_config(cls, **kwargs) -> InitConfig:
        return InitConfig.create(cls, **kwargs)
