"""Module for functions to convert images into tabular data"""

import json
from os.path import splitext, join, basename
from typing import Union, Tuple

import pandas as pd
from dagster import op, Field, OpExecutionContext
from hydra.types import ConvertMode
from hydra.utils import instantiate
from tqdm import tqdm

from niceml.config.hydra import HydraInitField
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_location_w_path,
    open_location,
)
from niceml.utilities.imagegeneration import convert_image_to_df_row
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.ioutils import list_dir, read_image, write_parquet
from niceml.utilities.splitutils import clear_folder


@op(
    config_schema={
        "output_location": Field(
            dict, description="Foldername where the images are stored"
        ),
        "name_delimiter": Field(
            str, default_value="_", description="Delimiter used within the filenames"
        ),
        "sub_dir": Field(
            str, default_value="", description="Subdirectory to save the split images"
        ),
        "recursive": Field(
            bool,
            default_value=True,
            description="Flag if the input folder should be searched recursively",
        ),
        "clear_folder": Field(
            bool,
            default_value=False,
            description="Flag if the output folder should be cleared before the split",
        ),
        "target_image_shape": HydraInitField(
            ImageSize,
            description="Image size to which the images should be scaled",
        ),
    }
)
def image_to_tabular_data(context: OpExecutionContext, input_location: dict):
    """
    The image_to_tabular_data function takes in a location of images
    and converts them to tabular data.

    Args:
        context: OpExecutionContext: Pass in the configuration of the operation
        input_location: dict: Specify the location of the input data

    Returns:
        The output_location
    """
    op_config = json.loads(json.dumps(context.op_config))

    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)

    output_location: Union[dict, LocationConfig] = instantiated_op_config[
        "output_location"
    ]
    if len(instantiated_op_config["sub_dir"]) > 0:
        output_location = join_location_w_path(
            output_location, instantiated_op_config["sub_dir"]
        )
    if instantiated_op_config["clear_folder"]:
        clear_folder(output_location)
    name_delimiter: str = instantiated_op_config["name_delimiter"]
    recursive: bool = instantiated_op_config["recursive"]
    target_size: Tuple[int, int] = instantiated_op_config["target_image_shape"]

    with open_location(input_location) as (input_fs, input_root):
        image_files = [
            cur_file
            for cur_file in list_dir(
                input_root, recursive=recursive, file_system=input_fs
            )
            if splitext(cur_file)[1] == ".png"
        ]
        df_rows = []
        for cur_file in tqdm(image_files):
            img = read_image(join(input_root, cur_file), file_system=input_fs)
            label = splitext(cur_file)[0].split(sep=name_delimiter)[-1]
            df_rows.append(
                convert_image_to_df_row(
                    identifier=basename(cur_file),
                    label=label,
                    image=img,
                    target_size=target_size,
                )
            )
        dataframe: pd.DataFrame = pd.DataFrame(df_rows)

        with open_location(output_location) as (output_fs, output_root):
            write_parquet(
                dataframe=dataframe,
                filepath=join(output_root, "numbers_tabular_data.parq"),
                file_system=output_fs,
            )
    return output_location
