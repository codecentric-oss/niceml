"""Module for RegDataDescription"""
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


class FeatureTypes:
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
        if feature_type not in FeatureTypes.get_available_features():
            raise ModeNotImplementedError(
                f"Feature type {feature['type']} not implemented"
            )
        count += (
            1
            if feature_type in [FeatureTypes.BINARY, FeatureTypes.SCALAR]
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
            assert target["type"] == "scalar"
            target_keys.append(target["key"])
        return target_keys

    def get_input_entry_names(self) -> List[str]:
        """Returns names of input entries"""
        input_keys: List[str] = []
        for cur_input in self.inputs:
            if cur_input["type"] in [FeatureTypes.SCALAR, FeatureTypes.BINARY]:
                input_keys.append(cur_input["key"])
            elif cur_input["type"] == FeatureTypes.CATEGORICAL:
                input_keys += [
                    f"{cur_input['key']}{x:03d}"
                    for x in range(cur_input["value_count"])
                ]

        return input_keys

    def get_min_max_vals(self) -> Dict[str, Tuple[int, int]]:
        """Get min and max values for categorical and binary input values"""
        min_max_dict: Dict[str, Tuple[int, int]] = {}
        for input_vector in self.inputs:
            if input_vector["type"] == FeatureTypes.BINARY:
                min_max_dict[input_vector["key"]] = (0, 1)
            elif input_vector["type"] == FeatureTypes.CATEGORICAL:
                min_max_dict[input_vector["key"]] = (0, input_vector["value_count"] - 1)

        return min_max_dict


def load_data_infos(yaml_path: str) -> RegDataDescription:  # QUEST: still used?
    """Loads and returns RegDataDescription from yaml-path"""
    with open(yaml_path, "r") as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    return RegDataDescription(**data)


def reg_data_description_factory(
    train_data_location: Union[dict, LocationConfig],
    train_set_file_name: str,
    filter_function: FunctionType,
    **kwargs,
) -> RegDataDescription:
    """Factory for creating RegDataDescription from train data"""
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
