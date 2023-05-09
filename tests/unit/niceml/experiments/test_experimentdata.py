import pytest

from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimenterrors import AmbigousFilenameError


def test_get_rel_file_exp_path_returns_correct_path(experiment_data: ExperimentData):
    experiment_data.all_exp_files = [
        "path/to/experiment/data.csv",
        "path/to/experiment/results.json",
    ]
    file = "data.csv"
    expected_path = "path/to/experiment/data.csv"
    assert experiment_data.get_rel_file_exp_path(file) == expected_path


def test_get_rel_file_exp_path_returns_correct_path2(experiment_data: ExperimentData):
    experiment_data.all_exp_files = [
        "path/to/experiment/data.csv",
        "path/to/experiment/results.json",
    ]
    file = "data"
    expected_path = "path/to/experiment/data.csv"
    assert experiment_data.get_rel_file_exp_path(file) == expected_path


def test_get_rel_file_exp_path_handles_missing_file(experiment_data: ExperimentData):
    experiment_data.all_exp_files = [
        "path/to/experiment/data.csv",
        "path/to/experiment/results.json",
    ]
    file = "missing_file.csv"
    with pytest.raises(FileNotFoundError):
        experiment_data.get_rel_file_exp_path(file)


def test_get_rel_file_exp_path_handles_ambiguous_file(experiment_data: ExperimentData):
    experiment_data.all_exp_files = [
        "path/to/experiment/data.csv",
        "path/to/experiment/results.json",
        "path/to/experiment/data.txt",
    ]
    file = "data"
    with pytest.raises(AmbigousFilenameError):
        experiment_data.get_rel_file_exp_path(file)


def test_get_rel_file_exp_path_handles_files_with_different_extensions(
    experiment_data: ExperimentData,
):
    experiment_data.all_exp_files = [
        "path/to/experiment/data.csv",
        "path/to/experiment/results.json",
        "path/to/experiment/data.txt",
    ]
    file = "data.csv"
    expected_path = "path/to/experiment/data.csv"
    assert experiment_data.get_rel_file_exp_path(file) == expected_path
