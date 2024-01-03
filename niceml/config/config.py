"""Module providing configuration-related functionality.

This module defines classes and functions for working with configurations in the context of the Dagster framework
and niceML's Hydra integration.
"""
import json
import logging
from abc import ABC
from dataclasses import asdict, dataclass
from inspect import isabstract
from tempfile import TemporaryDirectory, mkstemp
from typing import Optional, Any, Dict, Iterable

import yaml
from dagster import Config as DagsterConfig, config_mapping
from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from hydra.utils import instantiate, ConvertMode
from pydantic import Field, create_model

from niceml.scripts.hydraconfreader import load_hydra_conf
from niceml.utilities.omegaconfutils import register_niceml_resolvers


class Config(DagsterConfig, ABC):
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
        # TODO: infer arguments from target_class
        conf_class = create_model(
            f"Conf{target_class.__name__}",
            _target_=get_class_path(target_class),
            **kwargs,
            __base__=cls,
        )
        return conf_class(_target_=get_class_path(target_class), **kwargs)

    @classmethod
    def create_conf(cls, target_class, **kwargs):
        """Creates an instance of a pydantic BaseModel which have the same fields as given in kwargs"""
        conf_class = create_model(
            f"Conf{target_class.__name__}",
            target=(str, Field(default=get_class_path(target_class), alias="_target_")),
            **kwargs,
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

    @classmethod
    def create_config(cls, target_class):
        """Create a config class from a target class"""
        return cls(_target_=get_class_path(target_class))


def create_init_config(instance) -> InitConfig:
    """Create an InitConfig instance based on the provided instance's variables.

    Args:
        instance: An object with variables to be used in creating the InitConfig.

    Returns:
        An instance of the InitConfig class.
    """
    try:
        values = vars(instance)
    except TypeError:
        raise TypeError(type(instance))

    parsed_values = {key: parse_value(value) for key, value in values.items()}
    return InitConfig.create_conf(target_class=type(instance), **parsed_values)()


def parse_value(value):
    """Recursively parse a value, handling various types and creating InitConfig instances as needed.
    The value could be a `BaseModel`, an `InitConfig` or a default python datatype.
    Args:
        value: The value to be parsed.

    Returns:
        The parsed value.
    """
    if isinstance(value, (int, str, float, bool)):
        return value
    elif value is None:
        return None
    elif isinstance(value, (list, tuple)):
        return [parse_value(item) for item in value]
    elif isinstance(value, dict):
        return {key: parse_value(value) for key, value in value.items()}
    else:
        return create_init_config(value)


def instantiate_from_yaml(
    yaml_path: str, file_system: Optional[AbstractFileSystem] = None
) -> Any:
    """uses hydra instantiate to a yaml config"""
    file_system = file_system or LocalFileSystem()
    with file_system.open(yaml_path, "r", encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)

    return instantiate(data)


def prepend_hydra_search_paths(
    config: Dict[str, Any], searchpaths: Iterable[str]
) -> Dict[str, Any]:
    """Add searchpaths to config under hydra/searchpath."""
    config_hydra = config.get("hydra", {})
    config_hydra_searchpaths = list(searchpaths) + config_hydra.get("searchpath", [])
    return {**config, "hydra": {**config_hydra, "searchpath": config_hydra_searchpaths}}


def hydra_conf_mapping_factory(drop: Iterable[str] = ("globals",)):
    """
    Load hydra configuration from ``config``.

    Args:
        config: Configuration to be processed with hydra.
        drop: Keys to remove from the processed configuration after processing
               with hydra. Useful to define configuration variables that shall be used
               for interpolation during processing but not enter the processed
               configuration. Default: ``("globals",)``.
    """

    @config_mapping
    def hydra_conf_mapping(config: Dict[str, Any]):
        register_niceml_resolvers()
        config = json.loads(json.dumps(config))
        config_dir = TemporaryDirectory()  # pylint: disable=consider-using-with

        _, config_file = mkstemp(suffix=".yaml", dir=config_dir.name, text=True)
        with open(config_file, "wt", encoding="utf-8") as file:
            yaml.dump(config, file, Dumper=yaml.SafeDumper)

        conf = load_hydra_conf(config_file)
        try:
            config_dir.cleanup()
        except (PermissionError, NotADirectoryError):
            pass

        conf = {key: value for key, value in conf.items() if key not in set(drop)}
        return conf

    return hydra_conf_mapping


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
