"""Module for KerasModelLoader"""
from os.path import join
from tempfile import TemporaryDirectory
from typing import Any, Optional

from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from pydantic import Field

# pylint: disable=import-error
from tensorflow.keras.models import load_model

from niceml.config.config import InitConfig
from niceml.mlcomponents.modelcompiler.modelcustomloadobjects import (
    ModelCustomLoadObjects,
)
from niceml.mlcomponents.modelloader.modelloader import ModelLoader


class KerasModelLoader(
    ModelLoader, InitConfig
):  # pylint: disable=too-few-public-methods
    """Interface implementation to load a keras model"""

    model_custom_objects: ModelCustomLoadObjects = Field(
        default_factory=ModelCustomLoadObjects,
        description="custom objects to load the model. In Keras it is possible to pass custom objects during model loading.",
    )
    compile_model: bool = Field(
        default=True, description="Flag if the model should be compiled after loading"
    )

    def __call__(
        self,
        model_path: str,
        file_system: Optional[AbstractFileSystem] = None,
    ) -> Any:
        """Loads the model at the given path"""
        file_system = file_system or LocalFileSystem()
        with TemporaryDirectory() as tmp_dir:
            tmp_model_path = join(tmp_dir, "model.hdf5")
            with open(tmp_model_path, "wb") as tmp_model_file, file_system.open(
                model_path, "rb"
            ) as model_file:
                tmp_model_file.write(model_file.read())

            model = load_model(
                tmp_model_path, self.model_custom_objects(), compile=self.compile_model
            )
        return model
