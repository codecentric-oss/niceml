"""Module for RestAPI abstract base class"""

from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Optional, Union, Callable

from fastapi import FastAPI
from hydra.utils import instantiate, ConvertMode

from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    open_location,
    join_fs_path,
)
from niceml.utilities.ioutils import read_yaml


class Lifespan:
    """Helper class implementing the lifespan task of an FastAPI app"""

    def __init__(self, bundle_location: Optional[Union[dict, LocationConfig]], assets: dict):
        """
        Sets up the instance of a FastAPI Lifespan object, and defines what attributes it has.
        In this case, we are setting up a BundleConfig with two attributes: assets and
        bundle_location.

        Args:
            bundle_location: The location of the bundle
            assets: The assets that are loaded from the bundle
        """
        self.assets = assets
        self.bundle_location = bundle_location

    def get_lifespan(self) -> Callable:
        """
        The `get_lifespan function` is a factory function that returns an async context manager.
        The returned context manager will be used by FastAPI to manage the lifespan of the app.
        When the app is first loaded, it will open up the bundle location and read in all
        of its assets. It then yields control back to FastAPI so that it can continue with
        loading other plugins and starting up.

        Returns:
            A function that loads tha assets and that is a context manager
        """

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            with open_location(self.bundle_location) as (bundle_fs, bundle_root):
                bundle_info = read_yaml(
                    filepath=join_fs_path(bundle_fs, bundle_root, "bundle_info.yaml"),
                    file_system=bundle_fs,
                )

                for asset_name, asset_content in bundle_info["assets"].items():
                    instantiated_asset = instantiate(
                        asset_content["loader"],
                        _convert_=ConvertMode.ALL,
                    )
                    instantiated_kwargs = instantiate(
                        asset_content["kwargs"],
                        _convert_=ConvertMode.ALL,
                    )

                    self.assets[asset_name] = instantiated_asset(
                        join_fs_path(
                            bundle_fs,
                            bundle_info["working_directory"],
                            asset_content["path"],
                        ),
                        instantiated_kwargs,
                    )
            yield
            self.assets.clear()

        return lifespan


class RestApi(FastAPI):
    """Sets up a FastAPI app and loads all the assets from
    bundle_info.yaml into memory"""

    def __init__(self, bundle_location: Optional[Union[dict, LocationConfig]] = None, **kwargs):
        """
        Instantiate a RestAPI. It sets up a FastAPI app and loads all the assets from
        bundle_info.yaml into memory.

        Args:
            bundle_location: The location of the bundle
        """
        lifespan = Lifespan(bundle_location or {"uri": "./"}, defaultdict(dict))
        super().__init__(lifespan=lifespan.get_lifespan(), **kwargs)
        self.assets = lifespan.assets
        self.bundle_location = lifespan.bundle_location
