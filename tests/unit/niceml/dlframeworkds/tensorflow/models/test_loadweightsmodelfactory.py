from os.path import join
from tempfile import TemporaryDirectory

import pytest
from keras.models import Model

from niceml.data.datadescriptions.clsdatadescription import ClsDataDescription
from niceml.dlframeworks.tensorflow.models.loadweightsmodelfactory import (
    LoadWeightsModelFactory,
)
from niceml.dlframeworks.tensorflow.models.mobilenet import OwnMobileNetModel
from niceml.utilities.fsspec.locationutils import LocationConfig
from niceml.utilities.imagesize import ImageSize


@pytest.fixture
def tmp_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp


def test_loadweights_create_model(tmp_dir: str):
    mobile_factory = OwnMobileNetModel()
    model_path = join(tmp_dir, "model.hdf5")
    data_desc = ClsDataDescription(
        classes=["1", "2", "3"], target_size=ImageSize(512, 512)
    )
    mobile_net: Model = mobile_factory.create_model(data_desc)
    mobile_net.save_weights(model_path)
    weights_conf = LocationConfig(uri=model_path)
    load_weights_factory = LoadWeightsModelFactory(mobile_factory, weights_conf)
    loaded_model = load_weights_factory.create_model(data_desc)
    assert isinstance(loaded_model, Model)
