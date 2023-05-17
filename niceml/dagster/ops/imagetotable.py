"""Module for functions to convert images into tabular data"""

import json
from collections import defaultdict
from os.path import splitext, join, basename
from pathlib import Path
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
        "target_image_size": HydraInitField(
            ImageSize,
            description="Image size to which the images should be scaled",
        ),
        "use_dirs_as_subsets": Field(
            bool,
            default_value=True,
            description="Flag if the subdirectories should be used as subset names",
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
    target_size: Tuple[int, int] = instantiated_op_config["target_image_size"]
    use_dirs_as_subsets: bool = instantiated_op_config["use_dirs_as_subsets"]

    with open_location(input_location) as (input_fs, input_root):
        image_files = [
            cur_file
            for cur_file in list_dir(
                input_root, recursive=recursive, file_system=input_fs
            )
            if splitext(cur_file)[1] == ".png"
        ]
        df_row_dict = defaultdict(list)
        for cur_file in tqdm(image_files):
            img = read_image(join(input_root, cur_file), file_system=input_fs)
            label = splitext(cur_file)[0].split(sep=name_delimiter)[-1]
            if use_dirs_as_subsets:
                target_name = Path(cur_file).parts[0]

            else:
                target_name = "_all_"
            df_row_dict[target_name].append(
                convert_image_to_df_row(
                    identifier=basename(cur_file),
                    label=label,
                    image=img,
                    target_size=target_size,
                )
            )

        for subset_name, cur_df_row in df_row_dict.items():
            subset_name = f"_{subset_name}" if subset_name != "_all_" else ""
            dataframe: pd.DataFrame = pd.DataFrame(cur_df_row)

            with open_location(output_location) as (output_fs, output_root):
                write_parquet(
                    dataframe=dataframe,
                    filepath=join(output_root, f"numbers_tabular_data{subset_name}.parq"),
                    file_system=output_fs,
                )
    return output_location
