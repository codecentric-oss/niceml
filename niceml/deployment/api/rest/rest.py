"""Module for RestAPI abstract base class"""

from abc import ABC, abstractmethod
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Optional, Union, Any

from fastapi import FastAPI
from hydra.utils import instantiate, ConvertMode

from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    open_location,
    join_fs_path,
)
from niceml.utilities.ioutils import read_yaml

import uvicorn


class RestApi(ABC):
    """Sets up a FastAPI app and loads all the assets from
    bundle_info.yaml into memory"""

    def __init__(self, bundle_location: Optional[Union[dict, LocationConfig]] = None):
        """
        Instantiate a RestAPI. It sets up a FastAPI app and loads all the assets from
        bundle_info.yaml into memory.

        Args:
            bundle_location: The location of the bundle
        """
        self.bundle_location = bundle_location or {"uri": "./"}
        self.assets = defaultdict(dict)

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
            # Clean up the ML models and release the resources
            self.clean()

        self.app = FastAPI(lifespan=lifespan)
        self.setup_routes()

    def clean(self):
        """
        The clean function is called clean up any assets that are no longer needed.
        """
        self.assets.clear()

    def setup_routes(self):
        """
        The setup_routes function is used to define the routes that
        will be available in your API. It should be called after all other setup
        functions have been called, but before starting the server.
        """

        @self.app.post("/predict")
        async def detect_structure(input_data: dict) -> dict:
            return self._predict(input_data)

        @self.app.get("/exp_info")
        async def get_exp_info() -> dict:
            return self.assets["exp_info"]

        self.add_routes()

    @abstractmethod
    def _predict(self, input_data: dict) -> Any:
        """
        The _predict function is the main function of a model. It takes in an input_data dictionary
        and returns the prediction results. The input_data dictionary will contain all the data
        that was passed to the predict() function, but it may also contain additional data that
        was added by other functions (e.g., preprocessors).

        Args:
            input_data: dict: The data that will be used to make a prediction

        Returns:
            A prediction result
        """

    @abstractmethod
    def add_routes(self):
        """
        Adds routes to the application.

        Args:
            self: Represent the instance of the class
        """

    def run(self, host: str = "127.0.0.1", port: int = 8000):
        """
        The run function is the entry point for running the FastAPI application.
        It will start an uvicorn server, to serve the API.


        Args:
            host: The host ip address of the FastAPI application
            port: The port number that the server will listen on
        """
        uvicorn.run(self.app, host=host, port=port)
