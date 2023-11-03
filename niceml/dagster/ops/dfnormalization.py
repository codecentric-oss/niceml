"""Module for dataframe normalization op"""

import json
from typing import List, Any

import pandas as pd
from attrs import asdict
from dagster import op, Field, OpExecutionContext
from hydra.utils import instantiate, ConvertMode
from tqdm import tqdm

from niceml.data.normalization.minmax import (
    normalize_scalar_column,
    normalize_categorical_column,
    normalize_binary_column,
)
from niceml.data.normalization.normalization import NormalizationInfo
from niceml.utilities.fsspec.locationutils import (
    open_location,
    join_fs_path,
)
from niceml.utilities.ioutils import (
    list_dir,
    read_parquet,
    write_yaml,
    write_parquet,
)


@op(
    config_schema={
        "scalar_feature_keys": Field(
            Any,
            description="Column names to be normalized with scalar values (list or function)",
            default_value=[],
        ),
        "binary_feature_keys": Field(
            Any,
            description="Column names to be normalized with binary values (list or function)",
            default_value=[],
        ),
        "categorical_feature_keys": Field(
            Any,
            description="Column names to be normalized with categorical values (list or function)",
            default_value=[],
        ),
        "output_parq_location": Field(
            dict, description="Target location for the normalized parq files"
        ),
        "output_norm_feature_info_file_name": Field(
            str,
            description="File name for the file containing the normalization "
            "information of the features ",
            default_value="normalization_info.yaml",
        ),
        "recursive": Field(bool, description="", default_value=False),
    }
)
def df_normalization(context: OpExecutionContext, input_location: dict) -> dict:
    """
    The df_normalization function takes in a dataframe and normalizes the features
    specified in `scalar_feature_keys`, `categorical_feature_keys` and `binary_feature_keys`.
    The parameters for the feature keys can be a function that returns the feature keys as
    a list or a list of feature keys. The function returns a normalized parquet file with
    all columns normalized specified in feature_keys, as well as an output yaml file
    containing information about how each feature was normalized. The input_parq_location
    is where the input parquet files are located, while output_parq_location is where you
    want to save your new dataframes and norm info yaml.

    Args:
        context: OpExecutionContext: Get the op_config
        input_location: dict: Specify the location of the input data

    Returns:
        The output_parq_location, which is the location of the normalized parquet files
        and norm info
    """
    op_config = json.loads(json.dumps(context.op_config))
    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)
    output_parq_location: dict = instantiated_op_config["output_parq_location"]
    scalar_feature_keys: List[str] = instantiated_op_config["scalar_feature_keys"]

    binary_feature_keys: List[str] = instantiated_op_config["binary_feature_keys"]

    categorical_feature_keys: List[str] = instantiated_op_config[
        "categorical_feature_keys"
    ]
    output_norm_feature_info_file_name: str = instantiated_op_config[
        "output_norm_feature_info_file_name"
    ]

    with open_location(input_location) as (input_fs, input_root):
        input_files = list_dir(
            join_fs_path(input_fs, input_root),
            file_system=input_fs,
            recursive=instantiated_op_config["recursive"],
        )
        loaded_data_list: List[pd.DataFrame] = []
        for input_file in input_files:
            cur_df = read_parquet(
                file_system=input_fs,
                filepath=join_fs_path(input_fs, input_root, input_file),
            )
            cur_df["orig_file_name"] = [input_file for _ in range(len(cur_df))]
            loaded_data_list.append(cur_df)

        data = pd.concat(loaded_data_list)

        info_list: List[NormalizationInfo] = []
        for scalar_feature in tqdm(
            scalar_feature_keys, desc="Normalize scalar features"
        ):
            data, scalar_norm_info = normalize_scalar_column(data, scalar_feature)
            info_list.append(scalar_norm_info)
        for categorical_feature in tqdm(
            categorical_feature_keys, desc="Normalize categorical features"
        ):
            data, categorical_norm_info = normalize_categorical_column(
                data, categorical_feature
            )
            info_list.append(categorical_norm_info)
        for binary_feature in tqdm(
            binary_feature_keys, desc="Normalize binary features"
        ):
            data, binary_norm_info = normalize_binary_column(data, binary_feature)
            info_list.append(binary_norm_info)

        with open_location(output_parq_location) as (output_fs, output_root):
            info_dict_list: List[dict] = [asdict(info) for info in info_list]

            write_yaml(
                data={"norm_infos": info_dict_list},
                file_system=output_fs,
                filepath=join_fs_path(
                    output_fs, output_root, output_norm_feature_info_file_name
                ),
            )
            for file in input_files:
                write_parquet(
                    dataframe=data[data["orig_file_name"] == file].drop(
                        columns="orig_file_name"
                    ),
                    filepath=join_fs_path(output_fs, output_root, file),
                    file_system=output_fs,
                )

    return output_parq_location
