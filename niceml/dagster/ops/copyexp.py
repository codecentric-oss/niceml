"""Module containing dagster op which copies experiments"""
import logging
from os.path import basename, join
from typing import List

from fsspec import AbstractFileSystem
from tqdm import tqdm

from niceml.dagster.resources.locations import Location
from niceml.experiments.experimentinfo import get_exp_id_from_name
from dagster import Field, OpExecutionContext, op


@op(
    config_schema=dict(
        input_loc_name=Field(str, description="Name of the input location ressource"),
        output_loc_name=Field(str, description="Name of the output location ressource"),
        experiment_id=Field(
            str, description="Alphanumeric 4-char string to identify the experiment"
        ),
    ),
    required_resource_keys={"locations"},
)
def copy_exp(context: OpExecutionContext):
    """Copy experiment from one to another."""
    input_location: Location = context.resources.locations[
        context.op_config["input_loc_name"]
    ]
    output_location: Location = context.resources.locations[
        context.op_config["output_loc_name"]
    ]
    exp_id: str = context.op_config["experiment_id"]
    input_fs: AbstractFileSystem
    output_fs: AbstractFileSystem
    with input_location.open_fs_path() as (input_fs, in_path):
        exp_path_list: List[str] = [
            x for x in input_fs.ls(in_path) if get_exp_id_from_name(x) == exp_id
        ]
        if len(exp_path_list) == 1:
            exp_path = exp_path_list[0]
            in_mapper = input_fs.get_mapper(exp_path)
            exp_path_name = basename(exp_path)
            with output_location.open_fs_path() as (output_fs, out_fs_path):
                out_exp_path = join(out_fs_path, exp_path_name)
                out_mapper = output_fs.get_mapper(out_exp_path)
                logging.getLogger(__name__).info("Starting to copy experiment data")
                for key in tqdm(in_mapper):
                    out_mapper[key] = in_mapper[key]
            logging.getLogger(__name__).info("Removing old experiment data")
            input_fs.rm(exp_path, True)
        elif len(exp_path_list) == 0:
            logging.getLogger(__name__).warning("No exp found with the id: %s", exp_id)
        else:
            logging.getLogger(__name__).warning(
                "Multiple exps found with id: %s", exp_id
            )
