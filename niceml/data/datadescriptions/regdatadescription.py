"""Module for RegDataDescription"""
from dataclasses import dataclass
from typing import Dict, List, Tuple

import yaml

from niceml.data.datadescriptions.inputdatadescriptions import InputVectorDataDescription
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputVectorDataDescription,
)


def get_feature_size(features: List[dict]) -> int:
    """Returns size of features in 'features' dictionary"""
    count = 0
    for feature in features:
        assert feature["type"] in ["scalar", "categorical"]
        count += 1 if feature["type"] == "scalar" else feature["value_count"]
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
        for i in self.inputs:
            if i["type"] == "scalar":
                input_keys.append(i["key"])
            elif i["type"] == "categorical":
                input_keys += [f"{i['key']}{x:03d}" for x in range(i["value_count"])]

        return input_keys

    def get_min_max_vals(self) -> Dict[str, Tuple[int, int]]:
        """Get min and max values for categorical and binary input values"""
        min_max_dict: Dict[str, Tuple[int, int]] = {}
        for input_vector in self.inputs:
            if input_vector["type"] == "binary":
                min_max_dict[input_vector["key"]] = (0, 1)
            elif input_vector["type"] == "categorical":
                min_max_dict[input_vector["key"]] = (0, input_vector["value_count"] - 1)

        return min_max_dict


def load_data_infos(yaml_path: str) -> RegDataDescription:  # QUEST: still used?
    """Loads and returns RegDataDescription from yaml-path"""
    with open(yaml_path, "r") as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    return RegDataDescription(**data)
