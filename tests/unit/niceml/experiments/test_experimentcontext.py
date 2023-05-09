from os.path import isdir, join
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
import pytest
from PIL import Image

from niceml.experiments.experimentcontext import ExperimentContext
from niceml.utilities.fsspec.locationutils import LocationConfig


@pytest.fixture
def exp_tmp_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp


@pytest.fixture
def experiment_context(exp_tmp_dir):
    """Creates an ExperimentContext object using a temporary directory"""
    fs_config = LocationConfig(uri=join(exp_tmp_dir, "experiment"))
    run_id = "test_run_id"
    short_id = "test_short_id"
    return ExperimentContext(fs_config=fs_config, run_id=run_id, short_id=short_id)


def test_write_and_read_parquet(experiment_context):
    """Test that we can write and read a parquet file"""
    data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    data_path = "subfolder/data.parquet"
    experiment_context.write_parquet(data, data_path)
    result = experiment_context.read_parquet(data_path)
    pd.testing.assert_frame_equal(data, result)


def test_write_and_read_yaml(experiment_context):
    """Test that we can write and read a YAML file"""
    data = {"key1": "value1", "key2": "value2"}
    data_path = "subfolder/data.yaml"
    experiment_context.write_yaml(data, data_path)
    result = experiment_context.read_yaml(data_path)
    assert data == result


def test_write_and_read_csv(experiment_context):
    """Test that we can write and read a CSV file"""
    data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    data_path = "data.csv"
    experiment_context.write_csv(data, data_path)
    result = experiment_context.read_csv(data_path)
    pd.testing.assert_frame_equal(data, result)


def test_write_and_read_parquet_with_compression(experiment_context):
    """Test that we can write and read a compressed parquet file"""
    data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    data_path = "data.parquet.gzip"
    experiment_context.write_parquet(data, data_path, compression="gzip")
    result = experiment_context.read_parquet(data_path)
    pd.testing.assert_frame_equal(data, result)


def test_create_folder(experiment_context, exp_tmp_dir):
    """Test that it is possible to create a folder"""
    folder_name = "test1/test2"
    experiment_context.create_folder(folder_name)
    assert isdir(join(exp_tmp_dir, "experiment", folder_name))


def test_read_write_image(experiment_context, exp_tmp_dir):
    """Test that it is possible to read and write an image"""
    np_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    pil_image = Image.fromarray(np_image)
    image_path = "subfolder/image.png"
    experiment_context.write_image(pil_image, image_path)
    result = experiment_context.read_image(image_path)
    result_np = np.array(result)
    assert np.array_equal(np_image, result_np)
