"""Module for split_data op"""

import json
import logging
from typing import List

from attrs import asdict
from hydra.types import ConvertMode
from hydra.utils import instantiate

from niceml.utilities.copyutils import (
    CopyFileInfo,
    filter_for_required,
    process_copy_files,
)
from niceml.utilities.fsspec.locationutils import LocationConfig, join_location_w_path
from niceml.utilities.splitutils import clear_folder, create_copy_files_container
from dagster import Field, OpExecutionContext, op


@op(
    config_schema={
        "output_location": Field(dict, description="Folder to save the split images"),
        "set_infos": Field(list, description="Split information how to split the data"),
        "name_delimiter": Field(
            str, default_value="_", description="Character to seperate names."
        ),
        "sub_dir": Field(
            str, default_value="", description="Subdirectory to save the split images"
        ),
        "max_split": Field(
            int, default_value=1, description="Maximum split of the name (e.g. 1)"
        ),
        "recursive": Field(
            bool,
            default_value=False,
            description="Flag if the input folder should be searched recursively.",
        ),
        "clear_folder": Field(
            bool,
            default_value=False,
            description="Flag if the output folder should be cleared before the split.",
        ),
    }
)
def split_data(context: OpExecutionContext, input_location: dict):

    """Splits the data in input_location into subsets (set_infos)"""
    op_config = json.loads(json.dumps(context.op_config))

    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)

    output_location = instantiated_op_config["output_location"]
    if len(instantiated_op_config["sub_dir"]) > 0:
        output_location = join_location_w_path(
            output_location, instantiated_op_config["sub_dir"]
        )
    if instantiated_op_config["clear_folder"]:
        clear_folder(output_location)
    dataset_info_list = instantiated_op_config["set_infos"]
    recursive = instantiated_op_config["recursive"]
    delimiter_maxsplit = instantiated_op_config["max_split"]
    name_delimiter = instantiated_op_config["name_delimiter"]

    logging.getLogger(__name__).info("Read input folders")

    copy_files: List[CopyFileInfo] = create_copy_files_container(
        [""],
        input_location=input_location,
        recursive=recursive,
        dataset_info_list=dataset_info_list,
        delimiter_maxsplit=delimiter_maxsplit,
        name_delimiter=name_delimiter,
        output_location=output_location,
    )
    logging.getLogger(__name__).info("Filter already existing files")
    copy_files = filter_for_required(copy_files)
    logging.getLogger(__name__).info("Start to copy")
    process_copy_files(copy_files)
    if isinstance(output_location, LocationConfig):
        output_location = asdict(output_location)
    return output_location
