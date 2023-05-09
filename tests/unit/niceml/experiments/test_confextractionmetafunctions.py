from typing import List, Optional

import pytest

from niceml.experiments.confextractionmetafunction import (
    ConfigInfoExtractor,
    DictKeysToStringFormatFunc,
    git_hashtag_shortener,
    list_to_str_format_func,
    list_type_format_func,
    rsplit_format_func,
    str_or_type_format_func,
)
from niceml.experiments.experimentdata import ExperimentData


@pytest.mark.parametrize(
    "input_str,target",
    [("niceml.data.Model", "Model"), ("Model", "Model"), ("niceml.Model.", "Model")],
)
def test_rsplit_format_func(input_str, target):
    pred: str = rsplit_format_func(input_str)
    assert pred == target


@pytest.mark.parametrize(
    "input_value,target",
    [("test_str", "test_str"), (dict(_target_="niceml.Model"), "Model")],
)
def test_str_or_type_format_func(input_value, target: str):
    pred = str_or_type_format_func(input_value)
    assert pred == target


def test_str_or_type_format_func_failure():
    try:
        str_or_type_format_func(dict(test="name"))
    except KeyError:
        pass


@pytest.mark.parametrize(
    "input_value,target",
    [([dict(_target_="niceml.m1"), dict(_target_="niceml.m2")], ["m1", "m2"])],
)
def test_list_type_format_func(input_value, target: List[str]):
    pred = list_type_format_func(input_value)
    assert pred == target


@pytest.mark.parametrize(
    "input_value,target",
    [(None, None), ("test", "test"), ([1, 2, 3], "1,2,3"), (["as", "df"], "as,df")],
)
def test_list_to_str_format_func(input_value, target: Optional[str]):
    pred = list_to_str_format_func(input_value)
    assert pred == target


@pytest.mark.parametrize(
    "input_value,target",
    [
        (b"f0ebe459884861d523ce03909832241eaf1ec4a5\n", "f0ebe4"),
        ("f0ebe459884861d523ce03909832241eaf1ec4a5", "f0ebe4"),
        (None, None),
    ],
)
def test_git_hashtag_shortener(input_value, target):
    pred = git_hashtag_shortener(input_value)
    assert pred == target


@pytest.mark.parametrize(
    "key_list,target",
    [
        (["width", "height"], "256x256"),
        (["width"], "256"),
        (["width", "nokey"], "256"),
        (["no", "no"], None),
    ],
)
def test_dict_keys_to_string_format_func(key_list: List[str], target):
    info_dict = dict(_target_="niceml.imgsize.ImageSize", width=256, height=256)
    format_func = DictKeysToStringFormatFunc(key_list)
    pred = format_func(info_dict)
    assert pred == target


@pytest.mark.parametrize(
    "input_value,target",
    [
        ("test", "test"),
        (None, None),
    ],
)
def test_dict_keys_to_string_format_func_diff_types(input_value, target):
    format_func = DictKeysToStringFormatFunc([])
    pred = format_func(input_value)
    assert pred == target


@pytest.mark.parametrize(
    "info_path,target",
    [
        ([["datasets", "data_train", "sample_count"], ["test"]], 10),
        (["datasets", "test"], None),
        ([["datasets", "test"], ["datasets", "data_train", "sample_count"]], 10),
        (["datasets", "data_train", "sample_count"], 10),
    ],
)
def test_config_info_extractor_default(
    info_path, target, experiment_data: ExperimentData
):
    info_extractor = ConfigInfoExtractor("test", info_path)
    pred = info_extractor(experiment_data)
    assert pred == target
