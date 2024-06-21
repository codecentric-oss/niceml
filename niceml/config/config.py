"""Module providing configuration-related functionality.

This module defines classes and functions for working with configurations
in the context of the Dagster framework and niceML's Hydra integration.
"""

from __future__ import annotations

import inspect
from abc import ABC
from collections import defaultdict
from enum import Enum
from inspect import isabstract
from types import NoneType
from typing import (
    Optional,
    get_type_hints,
    Any,
    Tuple,
    Dict,
    List,
    Union,
    Generic,
    TypeVar,
)

from dagster import Config, PermissiveConfig, Field as DagsterField
from hydra.utils import instantiate, ConvertMode
from pydantic import Field, create_model, BaseModel, ConfigDict, SerializeAsAny


class InitConfig(PermissiveConfig):
    """
    Class representing the type of an attribute used in a Dagster Op configuration

    Attributes:
        target: Fully qualified class name of the class which is instantiated.
    """

    target: Optional[str] = Field(
        description="Target class which is instantiated.",
        serialization_alias="_target_",
    )

    def instantiate(self):
        """
        Instantiates the target class using the configuration parameters.

        Returns:
            Any: An instance of the target class.

        """
        instantiate_dict = self.model_dump(by_alias=True)
        print(instantiate_dict)
        if self.target is None and "_target_" not in instantiate_dict:
            instantiate_dict["_target_"] = get_class_path(type(self))
        instantiate_config = instantiate(instantiate_dict, _convert_=ConvertMode.ALL)
        print(instantiate_config)
        return instantiate_config

    def model_dump(self, *args, **kwargs):
        cur_dict = super().model_dump(
            *args,
            **kwargs,
        )
        cur_dict = self.replace_key_in_dict(cur_dict, "target", "_target_")

        if self.target is None and getattr(self, "_target_", None) is None:
            cur_dict[
                "_target_" if kwargs.get("by_alias", False) is True else "target"
            ] = get_class_path(type(self))
        return cur_dict

    # # TODO: To fields dict -> recursive
    # def get_config_as_field(self, model_dump: Optional[dict] = None) -> DagsterField:
    #     model_dump = model_dump or self.model_dump(by_alias=True)
    #     for key, value in model_dump.items():
    #         if isinstance(value, dict) and "_target_":
    #             model_dump[key] = self.get_config_as_field(value)
    #     return DagsterField(dict, default_value=model_dump)

    def replace_key_in_dict(self, config, old_key, new_key):
        """
        Recursively replace a key in a dictionary.

        :param config: The dictionary to search.
        :param old_key: The key to replace.
        :param new_key: The new key name.
        :return: The modified dictionary.
        """
        changed_config = {}
        for key, value in config.items():
            if key == old_key:
                changed_config[new_key] = value
            elif isinstance(value, dict):
                changed_config[key] = self.replace_key_in_dict(value, old_key, new_key)
            elif isinstance(value, list):
                changed_config[key] = []
                for idx, list_value in enumerate(value):
                    if isinstance(list_value, dict):
                        changed_config[key].append(
                            self.replace_key_in_dict(list_value, old_key, new_key)
                        )
                    else:
                        changed_config[key].append(list_value)
            else:
                changed_config[key] = value
        return changed_config

    @classmethod
    def create(cls, target_class, **kwargs):
        """Creates an instance of a pydantic BaseModel which have the same fields as
        given in kwargs"""
        conf_class = cls._create_conf_from_class(target_class)
        return conf_class(**kwargs, target=get_class_path(target_class))

    @classmethod
    def _create_conf_from_class(
        cls, target_class, protected_namespaces: Optional[Tuple[str]] = None, **kwargs
    ):
        """
        Creates a configuration class from a target class by introspecting its __init__ method.

        Args:
            cls: The base configuration class (`InitConfig`) to inherit from.
            target_class: The target class from which the configuration class will be created.

        Returns:
            The dynamically created configuration class as a Pydantic model.

        Examples:
            - For classes derived from InitConfig or Config, returns the target class itself.
            - Inspects the __init__ method of the target class and extracts parameter information.
            - Generates default values for parameters, parses that values with `parse_value_type`
              and creates a configuration class using 'pydantic.create_model'.
            - Handles Enum types by specifying a default value based on their underlying
              type (str or int).

        """
        if issubclass(target_class, (InitConfig, Config)):
            return target_class

        sig = inspect.signature(target_class.__init__)
        type_hints = get_type_hints(target_class.__init__)
        params = sig.parameters
        target_kwargs = kwargs or {}
        if issubclass(target_class, Enum):
            target_enum_type = str if issubclass(target_class, str) else int
            target_kwargs["value"] = (target_enum_type, ...)
        for name, param in params.items():
            if name in ["self", "args", "kwargs"]:
                continue
            current_type = parse_value_type(type_hints.get(name, Any))
            if param.default is not inspect._empty:
                target_kwargs[name] = (SerializeAsAny[current_type], param.default)
            else:
                target_kwargs[name] = (SerializeAsAny[current_type], ...)

        conf_class = create_model(
            f"Conf{target_class.__name__}",
            # target=(
            #     str,
            #     ...,
            # ),
            model_config=ConfigDict(protected_namespaces=protected_namespaces or ()),
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

    @staticmethod
    def create_dict_config_field(
        target_class, description: Optional[str] = None, **kwargs
    ):
        if description is None:
            description = f"Dict of instances of class: {target_class.__name__} {target_class.__doc__}"

        # TODO: Add key list ["train","validation",...]
        return Field(default={}, description=description)


def parse_value_type(value_type: type):
    """
    Recursively parses and constructs the corresponding type with inner types and returns
    its corresponding type or InitConfig if `value_type` is not a python basic type or
    is not defined in the 'typing' module (Dict, Tuple, Union, List, Optional).

    Args:
        value_type: The type to be parsed.

    Returns:
        The parsed type or InitConfig.

    Examples:
        - For basic types (int, str, float, bool, dict, list, tuple), returns the same type.
        - For Enum type, returns InitConfig.
        - For types defined in the 'typing' module (Dict, Tuple, Union, List, Optional),
          recursively parses and constructs the corresponding type with inner types.
        - In all other cases, returns InitConfig.

    """
    parsed_type = InitConfig

    if value_type in (int, str, float, bool, dict, list, tuple):
        return value_type
    elif value_type == Enum:
        return parsed_type
    elif hasattr(value_type, "__name__") and hasattr(value_type, "__module__"):
        fully_qualified_type_name = f"{value_type.__module__}.{value_type.__name__}"
        if hasattr(value_type, "__args__"):
            args = value_type.__args__
            if fully_qualified_type_name == "typing.Dict":
                parsed_type = Dict[parse_value_type(args[0]), parse_value_type(args[1])]
            elif fully_qualified_type_name == "typing.Tuple":
                parsed_type = Tuple[tuple([parse_value_type(arg) for arg in args])]
            elif fully_qualified_type_name == "typing.Union":
                parsed_type = Union[tuple([parse_value_type(arg) for arg in args])]
            elif fully_qualified_type_name == "typing.List":
                parsed_type = List[tuple([parse_value_type(arg) for arg in args])]
            elif fully_qualified_type_name == "typing.Optional":
                parsed_type = Optional[parse_value_type(args[0])]
        elif value_type.__module__ == "typing":
            return value_type
        elif inspect.isclass(value_type) and issubclass(value_type, BaseModel):
            parsed_type = value_type
        elif value_type is None or value_type == NoneType:
            parsed_type = value_type
    return parsed_type


def get_class_path(cls):
    """Get the path of a class"""
    return f"{cls.__module__}.{cls.__name__}"


class MapInitConfig(PermissiveConfig):
    def instantiate(self):
        """
        Instantiates the target class using the configuration parameters.

        Returns:
            Any: An instance of the target class.

        """
        return instantiate(self.dict(by_alias=True), _convert_=ConvertMode.ALL)

    @classmethod
    def create(cls, map_target_class, **kwargs):
        conf_class = cls.create_conf_from_values(map_target_class, **kwargs)
        return conf_class(**kwargs)

    @classmethod
    def create_conf_from_values(cls, map_target_class, **kwargs):
        field_kwargs = {}
        for key, value in kwargs.items():
            field_kwargs[key] = (
                type(value),
                value,
            )

        conf_class = create_model(
            f"ConfMap{map_target_class.__name__}",
            **field_kwargs,
            __base__=cls,
        )
        return conf_class

    @staticmethod
    def create_config_field(
        target_class,
        description: Optional[str] = None,
        **kwargs,
    ):
        """
        Used to configure Dagster Ops with a MapInitConfig

        Args:
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
    """
    Abstract class from which every class that is to be part of a
    Dagster Op configuration must inherit.
    """

    @classmethod
    def create_config(cls, **kwargs) -> InitConfig:
        """
        Class method to create a InitConfig representing class.

        Args:
            **kwargs: Attributes that are used later to instantiate the class.

        Returns:
            Class specific instance of InitConfig
        """
        return InitConfig.create(cls, **kwargs)
