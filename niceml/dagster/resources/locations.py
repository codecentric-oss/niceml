"""Dagster resource for accessing filesystem locations."""
import logging
import os
from contextlib import contextmanager
from copy import deepcopy
from logging import getLogger
from typing import Any, Dict, Iterator, Optional

from attr import asdict

from niceml.config.configschemas import build_config_schema, define, field, parse_config
from niceml.utilities.fsspec.locationutils import FSPath, LocationConfig, open_location
from dagster import InitResourceContext, resource  # pylint: disable=ungrouped-imports


class Location:
    """Filesystem plus path."""

    def __init__(self, config: LocationConfig):
        self._config = deepcopy(config)

    @contextmanager
    def open_fs_path(self) -> Iterator[FSPath]:
        """Return filesystem and path as context manager."""
        with open_location(asdict(self._config)) as (filesystem, path):
            yield (filesystem, path)

    @contextmanager
    def open(self, rel_path: str, *args, **kwargs) -> Iterator[Any]:
        """Open file at ``rel_path`` with ``*args`` and ``**kwargs``."""
        with self.open_fs_path() as (filesystem, path):
            absolute_path = os.path.join(path, rel_path)
            yield filesystem.open(absolute_path, *args, **kwargs)

    def __str__(self) -> str:
        """Return string representation of config."""
        return str(self._config)


@define
class LocationsResourceConfig:  # pylint: disable=too-few-public-methods
    """Configuration of file system locations."""

    locations: Dict[str, LocationConfig] = field(
        factory=dict,
        description="""Mapping of location names to filesystem+path configurations.
        The latter consist of a ``uri`` and optional ``fs_args`` and ``credentials``
        passed to fsspec_.""",
    )


class LocationsResource:  # pylint: disable=too-few-public-methods
    """Resource for accessing file system.

    Arguments:
      config: resource configuration.
    """

    def __init__(self, config: LocationsResourceConfig):
        location_items = config.locations.items()
        self._locations = {key: Location(value) for key, value in location_items}

    def __getitem__(self, location_name: str) -> Location:
        """Return configured location."""
        try:
            location = self._locations[location_name]
        except KeyError as exception:
            getLogger(__name__).error("location %s not configured", location_name)
            raise exception
        getLogger(__name__).debug("opening location %s (%s)", location_name, location)
        return location


@resource(config_schema=build_config_schema(LocationsResourceConfig))
def locations_resource(context: InitResourceContext):
    """Create LocationsResource according to the configuration."""
    config = parse_config(context.resource_config, LocationsResourceConfig)
    return LocationsResource(config)


_LOCATIONS_RESOURCE: Optional[LocationsResource] = None


@resource
def global_locations_resource(context: InitResourceContext):
    """Return `LocationsResource` and register it as module-level object ``FS``."""
    global _LOCATIONS_RESOURCE  # pylint: disable=global-statement
    _LOCATIONS_RESOURCE = locations_resource(context)
    return _LOCATIONS_RESOURCE


def get_location(location_name: str) -> Location:
    """Return location."""
    if _LOCATIONS_RESOURCE is None:
        logging.error(
            """Locations resource not configured. Define the resource
            ``global_fs_resource`` for your dagster job and require it for your op."""
        )
        raise ValueError("Locations resource not configured. See log for details.")
    return _LOCATIONS_RESOURCE[location_name]
