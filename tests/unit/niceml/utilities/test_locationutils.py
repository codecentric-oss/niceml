from os.path import join

import pytest
from cattr import structure
from cattrs.errors import ClassValidationError

from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    get_location_uri,
    join_location_w_path,
)


def test_join_fs_path():
    s3_path = "s3://bucket"
    filepath = "path/to/file"
    old_config = LocationConfig(uri=s3_path, fs_args={"an_arg": "value"})
    new_config = join_location_w_path(old_config, filepath)
    new_config_multiple = join_location_w_path(old_config, ["foldername", filepath])
    assert new_config.uri == join(s3_path, filepath)
    assert new_config.fs_args == old_config.fs_args
    assert new_config_multiple.uri == join(s3_path, "foldername", filepath)
    assert new_config_multiple.fs_args == old_config.fs_args
    assert old_config.uri == s3_path


def test_get_location_uri_with_fs_path_config():
    config = LocationConfig(uri="s3://my-bucket")
    assert get_location_uri(config) == "s3://my-bucket"


def test_get_location_uri_with_dict():
    config_dict = {"uri": "gs://my-bucket"}
    config = structure(config_dict, LocationConfig)
    assert get_location_uri(config) == "gs://my-bucket"


def test_get_location_uri_with_invalid_input():
    with pytest.raises(ClassValidationError):
        get_location_uri("invalid input")


def test_get_location_uri_with_missing_uri():
    with pytest.raises(ClassValidationError):
        config_dict = {"fs_args": {"key": "value"}}
        config = structure(config_dict, LocationConfig)
        get_location_uri(config)
