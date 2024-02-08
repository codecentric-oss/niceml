"""module for writing config files"""
from os.path import join
from typing import List, Union

import mlflow
from pydantic import BaseModel

from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import ExperimentFilenames


def write_op_config(
    op_conf: Union[dict, BaseModel],
    exp_context: ExperimentContext,
    op_name: str,
    remove_key_list: List[str],
):
    """Writes a dict as yamls. With one file per key"""
    op_conf_dict = (
        op_conf.dict(by_alias=True) if isinstance(op_conf, BaseModel) else op_conf
    )
    for key, values in op_conf_dict.items():
        removed_values = remove_key_recursive(values, remove_key_list)
        outfile = join(ExperimentFilenames.CONFIGS_FOLDER, op_name, f"{key}.yaml")
        mlflow.log_dict(removed_values, outfile)
        exp_context.write_yaml(removed_values, outfile)


def remove_key_recursive(data, key_list: List[str]):
    """Removes keys from a dict recursively. This is used for credentials."""
    if isinstance(data, list):  # handle lists
        return [remove_key_recursive(item, key_list) for item in data]
    elif isinstance(data, dict):  # handle dictionaries
        return {
            k: remove_key_recursive(v, key_list)
            for k, v in data.items()
            if k not in key_list
        }
    else:
        return data
