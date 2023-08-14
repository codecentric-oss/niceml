"""Module for RegDataDescription"""
import logging
from dataclasses import dataclass
from types import FunctionType
from typing import Dict, List, Tuple, Union

import yaml

from niceml.data.datadescriptions.inputdatadescriptions import (
    InputVectorDataDescription,
)
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputVectorDataDescription,
)
from niceml.data.datashuffler.uniformdistributionshuffler import ModeNotImplementedError
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    open_location,
    join_fs_path,
)
from niceml.utilities.ioutils import read_parquet


class FeatureType:
    """FeatureTypes are used for defining which kind of features are available."""

    SCALAR = "scalar"
    CATEGORICAL = "categorical"
    BINARY = "binary"

    @classmethod
    def get_available_features(cls) -> List[str]:
        """Returns list of available feature types"""
        return [cls.SCALAR, cls.CATEGORICAL, cls.BINARY]


def get_feature_size(features: List[dict]) -> int:
    """Returns size of features in 'features' dictionary"""
    count = 0
    for feature in features:
        feature_type = feature["type"]
        if feature_type not in FeatureType.get_available_features():
            raise ModeNotImplementedError(
                f"Feature type {feature['type']} not implemented"
            )
        count += (
            1
            if feature_type in [FeatureType.BINARY, FeatureType.SCALAR]
            else feature["value_count"]
        )
    return count


@dataclass
class RegDataDescription(InputVectorDataDescription, OutputVectorDataDescription):
    """DataDescription for Regression data. Uses vectors as input and output"""

    inputs: List[dict]
    targets: List[dict]

    def get_input_size(self) -> int:
        """Returns size of input vector(s)"""
        return get_feature_size(self.inputs)

    def get_output_size(self) -> int:
        """Returns size of output vector(s) (targets)"""
        return get_feature_size(self.targets)

    def get_dict(self) -> dict:
        """Returns dictionary of inputs and targets"""
        return dict(inputs=self.inputs, targets=self.targets)

    def get_output_entry_names(self) -> List[str]:
        """Returns names of targets"""
        target_keys = []
        for target in self.targets:
            if target["type"] != "scalar":
                raise ValueError("Target feature type is not scalar")
            target_keys.append(target["key"])
        return target_keys

    def get_input_entry_names(self) -> List[str]:
        """Returns names of input entries"""
        input_keys: List[str] = []
        for cur_input in self.inputs:
            if cur_input["type"] in [FeatureType.SCALAR, FeatureType.BINARY]:
                input_keys.append(cur_input["key"])
            elif cur_input["type"] == FeatureType.CATEGORICAL:
                input_keys += [
                    f"{cur_input['key']}{x:03d}"
                    for x in range(cur_input["value_count"])
                ]

        return input_keys

    def get_min_max_vals(self) -> Dict[str, Tuple[int, int]]:
        """Get min and max values for categorical and binary input values"""
        min_max_dict: Dict[str, Tuple[int, int]] = {}
        for input_vector in self.inputs:
            if input_vector["type"] == FeatureType.BINARY:
                min_max_dict[input_vector["key"]] = (0, 1)
            elif input_vector["type"] == FeatureType.CATEGORICAL:
                min_max_dict[input_vector["key"]] = (0, input_vector["value_count"] - 1)

        return min_max_dict


def load_data_infos(yaml_path: str) -> RegDataDescription:  # QUEST: still used?
    """Loads and returns RegDataDescription from yaml-path"""
    with open(yaml_path, "r") as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    return RegDataDescription(**data)


def inputs_prefix_factory(
    data_location: Union[dict, LocationConfig],
    prefix: str,
    feature_type: str,
    data_file_name: str = "train.parq",
) -> List[dict]:
    """
    The inputs_prefix_factory function is a factory function that returns a list of
    input features as dictionaries.

    Args:
        data_location: Specify the location of the data
        prefix: Filter the columns in the dataframe
        feature_type: Specify the type of feature
        data_file_name: Specify the name of the file to be read from data_location
    Returns:
        A list of input features as dictionaries
    """
    with open_location(data_location) as (
        data_fs,
        data_root,
    ):
        try:
            loaded_data = read_parquet(
                filepath=join_fs_path(data_fs, data_root, data_file_name),
                file_system=data_fs,
            )
            return [
                {"key": column, "type": feature_type}
                for column in loaded_data.columns
                if column.startswith(prefix)
            ]
        except FileNotFoundError:
            logger = logging.getLogger(__name__)
            logger.warning("Data file not found. Inputs will be empty.")
        return []


def reg_data_description_factory(
    train_data_location: Union[dict, LocationConfig],
    train_set_file_name: str,
    filter_function: FunctionType,
    **kwargs,
) -> RegDataDescription:
    """
    The reg_data_description_factory function is a factory function that returns a
    RegDataDescription object.The RegDataDescription object contains the inputs and targets
    of the regression data set.
    The reg_data_description_factory function takes in arguments for:
        - train_data_location: The location of the training data set
        - train_set_file name: The name of the training data set file
        - filter function: A filtering function to apply to each row in order to
                            extract input and target features from it

    Args:
        train_data_location: The location of the training data set
        train_set_file_name: The name of the training data set file
        filter_function: A filtering function to apply to each row in order to
                        extract input and target features from it
        **kwargs: Pass in additional arguments to the filter_functions

    Returns:
        A RagDataDescription with inputs and targets created by the filter_function
    """
    with open_location(train_data_location) as (
        regression_data_fs,
        regression_data_root,
    ):
        train_data = read_parquet(
            filepath=join_fs_path(
                regression_data_fs, regression_data_root, train_set_file_name
            ),
            file_system=regression_data_fs,
        )

        inputs: List[Dict[str, str]]
        targets: List[Dict[str, str]]

        inputs, targets = filter_function(data=train_data, **kwargs)

        return RegDataDescription(inputs=inputs, targets=targets)
