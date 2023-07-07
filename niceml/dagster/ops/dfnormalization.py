"""Module for dataframe normalization op"""

import json
from types import FunctionType
from typing import List, Optional

from attrs import asdict
from dagster import op, Field, OpExecutionContext
from hydra.utils import instantiate, ConvertMode
from tqdm import tqdm

from niceml.data.normalization.dataframe import normalize_col
from niceml.data.normalization.normalization import NormalizationInfo
from niceml.utilities.fsspec.locationutils import open_location, join_fs_path
from niceml.utilities.ioutils import (
    list_dir,
    read_parquet,
    write_yaml,
    write_parquet,
)


@op(
    config_schema={
        "input_parq_location": Field(dict, description=""),
        "feature_keys": Field(list, description="", default_value=[]),
        "feature_keys_function": Field(dict, description="", default_value={}),
        "output_parq_location": Field(dict, description=""),
        "output_norm_feature_info_file_name": Field(
            str, description="", default_value="normalization_info.yaml"
        ),
        "recursive": Field(bool, description="", default_value=False),
    }
)
def df_normalization(
    context: OpExecutionContext, input_location: Optional[dict] = None
) -> dict:
    """
    The df_normalization function takes in parquet files and normalizes the features
    specified in `feature_keys`. The function returns a normalized parquet file with
    all columns normalized specified in `feature_keys`, as well as an output yaml file
    containing information about how each feature was normalized. The input_parq_location
    is where the input parquet files are located, while output_parq_location is where you
    want to save your new dataframes and norm info yaml. feature keys are what you want
    to normalize.

    Args:
        context: OpExecutionContext: Access the op_config and other parameters
        input_location: Input location of the features parquet files

    Returns:
        The `output_parq_location` as a dict

    """
    op_config = json.loads(json.dumps(context.op_config))
    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)
    input_parq_location: dict = (
        input_location or instantiated_op_config["input_parq_location"]
    )
    output_parq_location: dict = instantiated_op_config["output_parq_location"]
    feature_keys: List[str] = instantiated_op_config["feature_keys"]
    feature_keys_function = instantiated_op_config["feature_keys_function"]
    output_norm_feature_info_file_name: str = instantiated_op_config[
        "output_norm_feature_info_file_name"
    ]

    with open_location(input_parq_location) as (input_fs, input_root):
        input_files = list_dir(
            join_fs_path(input_fs, input_root),
            file_system=input_fs,
            recursive=instantiated_op_config["recursive"],
        )

        for input_file in input_files:
            cur_df = read_parquet(
                file_system=input_fs,
                filepath=join_fs_path(input_fs, input_root, input_file),
            )

            info_list: List[NormalizationInfo] = []
            if isinstance(feature_keys_function, FunctionType):
                extended_feature_keys = feature_keys + feature_keys_function(cur_df)
            else:
                extended_feature_keys = feature_keys
            for feature in tqdm(extended_feature_keys, desc="Normalize features"):
                cur_df, feat_info = normalize_col(cur_df, feature)
                info_list.append(feat_info)

            with open_location(output_parq_location) as (output_fs, output_root):
                info_dict_list: List[dict] = [asdict(info) for info in info_list]

                write_yaml(
                    data={"norm_infos": info_dict_list},
                    file_system=output_fs,
                    filepath=join_fs_path(
                        output_fs, output_root, output_norm_feature_info_file_name
                    ),
                )

                write_parquet(
                    dataframe=cur_df,
                    filepath=join_fs_path(output_fs, output_root, input_file),
                    file_system=output_fs,
                )

    return output_parq_location
