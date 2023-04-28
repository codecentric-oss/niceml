"""This module contains functions to find experiment paths."""
from typing import List

from niceml.data.storages.fsspecstorage import FSSpecStorage
from niceml.experiments.experimenterrors import ExperimentNotFoundError
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.utilities.fsspec.locationutils import LocationConfig


def get_exp_filepath(fs_path_config: LocationConfig, exp_id: str):
    """Searches for the experimentpath with the given id.
    `latest` returns the newest experiment."""
    storage = FSSpecStorage(fs_path_config)
    exp_id_list: List[ExperimentInfo] = storage.list_experiments()
    exp_id_list = sorted(exp_id_list, key=lambda x: x.run_id)
    if exp_id == "latest":
        return exp_id_list[-1].exp_filepath
    exps_w_id = [cur_exp for cur_exp in exp_id_list if cur_exp.short_id == exp_id]
    if len(exps_w_id) == 0:
        raise ExperimentNotFoundError(
            f"Experiment with id: {exp_id} not found in path: {fs_path_config.uri}"
        )
    if len(exps_w_id) > 1:
        raise ExperimentNotFoundError(
            f"Multiple experiments with id: {exp_id} found in path: {fs_path_config.uri}"
        )
    return exps_w_id[0]
