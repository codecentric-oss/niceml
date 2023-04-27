"""Module for KerasModelLoader"""
from os.path import join
from tempfile import TemporaryDirectory
from typing import Any, Optional

from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem

# pylint: disable=import-error
from tensorflow.keras.models import load_model

from niceml.mlcomponents.modelcompiler.modelcustomloadobjects import (
    ModelCustomLoadObjects,
)
from niceml.mlcomponents.modelloader.modelloader import ModelLoader


class KerasModelLoader(ModelLoader):  # pylint: disable=too-few-public-methods
    """Interface implementation to load a keras model"""

    def __init__(self, compile_model: bool = False):
        self.compile_model = compile_model

    def __call__(
        self,
        model_path: str,
        model_custom_objects: ModelCustomLoadObjects,
        file_system: Optional[AbstractFileSystem] = None,
    ) -> Any:
        file_system = file_system or LocalFileSystem()
        with TemporaryDirectory() as tmp_dir:
            tmp_model_path = join(tmp_dir, "model.hdf5")
            with open(tmp_model_path, "wb") as tmp_model_file, file_system.open(
                model_path, "rb"
            ) as model_file:
                tmp_model_file.write(model_file.read())

            model = load_model(
                tmp_model_path, model_custom_objects(), compile=self.compile_model
            )
        return model
