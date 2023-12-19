"""Module for LoadWeightsModelFactory"""
from os.path import join
from tempfile import TemporaryDirectory
from typing import Any, Optional

from keras.models import Model

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.mlcomponents.models.modelfactory import ModelFactory
from niceml.utilities.fsspec.locationutils import LocationConfig, open_location


class LoadWeightsModelFactory(ModelFactory):  # pylint: disable=too-few-public-methods
    """model factory to load weights before training starts"""

    def __init__(
        self,
        model_factory: ModelFactory,
        weights_config: LocationConfig,
        loading_options: Optional[dict] = None,
    ):
        self.model_factory = model_factory
        self.weights_config = weights_config
        self.loading_options = loading_options or {}

    def create_model(self, data_description: DataDescription) -> Any:
        model: Model = self.model_factory.create_model(data_description)
        if self.weights_config is not None:
            with open_location(self.weights_config) as (file_system, model_path):
                with TemporaryDirectory() as tmp_dir:
                    tmp_model_path = join(tmp_dir, "model.hdf5")
                    with open(tmp_model_path, "wb") as tmp_model_file, file_system.open(
                        model_path, "rb"
                    ) as model_file:
                        tmp_model_file.write(model_file.read())

                    model.load_weights(tmp_model_path, **self.loading_options)
        return model
