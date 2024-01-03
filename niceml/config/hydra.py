import json
from tempfile import TemporaryDirectory, mkstemp
from typing import Optional, Any, Dict, Iterable

import yaml
from dagster import config_mapping
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
