"""Module containing all utils regarding hydra"""
import json
from inspect import isabstract
from tempfile import TemporaryDirectory, mkstemp
from typing import Any, Dict, Iterable, Optional

import yaml
from dagster import Field, Map, config_mapping
from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from hydra.utils import instantiate

from niceml.scripts.hydraconfreader import load_hydra_conf
from niceml.utilities.omegaconfutils import register_niceml_resolvers


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


class HydraInitField(Field):
    """Used to configure Dagster Ops"""

    def __init__(
        self,
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
            example_value: example value of the field shown in the documentation
            **kwargs: additional kwargs passed to the Field class
        """
        if description is None:
            description = target_class.__doc__
        if default_value is None:
            default_value = dict()
        if example_value is None:
            impl_str: str = "implementation_of_" if isabstract(target_class) else ""
            default_value = {"_target_": f"{impl_str}{target_class}"}
        super().__init__(
            dict, description=description, default_value=default_value, **kwargs
        )
        self.target_class = target_class
        self.example_value = example_value


class HydraMapField(Field):
    """Used to configure Dagster Ops"""

    def __init__(
        self,
        target_class,
        description: Optional[str] = None,
        default_value: Optional[dict] = None,
        example_value: Optional[dict] = None,
        **kwargs,
    ):
        """
        Used to configure Dagster Ops with a map

        Args:
            target_class: class which is instantiated from the op in the map
            description: description of the class or field
            default_value: default value of the field when nothing is provided
            example_value: example value of the field shown in the documentation
            **kwargs: additional kwargs passed to the Field class
        """
        if description is None:
            description = target_class.__doc__
        if default_value is None:
            default_value = dict()
        if example_value is None:
            impl_str: str = "implementation_of_" if isabstract(target_class) else ""
            example_value = {"value": {"_target_": f"{impl_str}{target_class}"}}
        super().__init__(
            Map(str, dict),
            description=description,
            default_value=default_value,
            **kwargs,
        )
        self.target_class = target_class
        self.example_value = example_value
