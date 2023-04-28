"""Module to access description for a remote storage location"""
from contextlib import contextmanager
from copy import deepcopy
from os.path import join
from typing import Any, Dict, Iterator, Tuple, Union

import cattr
from attr import asdict
from fsspec import AbstractFileSystem
from fsspec.core import url_to_fs

from niceml.config.configschemas import define, field

FSPath = Tuple[AbstractFileSystem, str]


@define
class LocationConfig:  # pylint: disable=too-few-public-methods
    """Access description for a remote storage location. The description is targeted at fsspec_."""

    uri: str = field(description="""URL to remote storage as expected by fsspec_.""")
    fs_args: Dict[str, Any] = field(
        description="""Optional filesystem arguments to be passed to fsspec_, see e.g.
  https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations""",
        factory=dict,
    )
    credentials: Dict[str, Any] = field(
        description="""Optional credentials to be passed as filesystem
        arguments to fsspec_.""",
        factory=dict,
    )

    def __str__(self) -> str:
        """Returns string representation without credential values"""
        info = asdict(self)
        info["credentials"] = list(info["credentials"])
        return str(info)


def join_location_w_path(
    location: Union[LocationConfig, dict], path: str
) -> LocationConfig:
    """Returns joined path to a LocationConfig"""
    parsed_config = (
        location
        if isinstance(location, LocationConfig)
        else cattr.structure(location, LocationConfig)
    )
    copied_config = deepcopy(parsed_config)
    # TODO: check how to get the correct separator from the filesystem
    copied_config.uri = join(copied_config.uri, path)
    return copied_config


def join_fs_path(file_system: AbstractFileSystem, *paths: str) -> str:
    """Returns joined given paths with the fsspec specific path seperator"""
    paths = [path for path in paths if len(path) > 0]
    return file_system.sep.join(paths)


def get_location_uri(location: Union[LocationConfig, dict]) -> str:
    """Returns the URI of a LocationConfig."""
    parsed_config = (
        location
        if isinstance(location, LocationConfig)
        else cattr.structure(location, LocationConfig)
    )
    return parsed_config.uri


@contextmanager
def open_location(config: Union[LocationConfig, Dict[str, Any]]) -> Iterator[FSPath]:
    """
    Creates a filesystem and path from configuration as a single context manager.
    The filesystem is "closed" (i.e. open connections are closed) when the context is left.
    """
    parsed_config = (
        config
        if isinstance(config, LocationConfig)
        else cattr.structure(config, LocationConfig)
    )
    credentials = deepcopy(parsed_config.credentials)
    fs_args = deepcopy(parsed_config.fs_args)
    filesystem, path = url_to_fs(parsed_config.uri, **credentials, **fs_args)
    try:
        yield filesystem, path
    finally:
        del filesystem
