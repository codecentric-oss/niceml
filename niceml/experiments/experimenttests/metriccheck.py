import operator as operator_module
from os.path import join
from typing import List, Optional, Union

import yaml
from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem

from niceml.experiments.experimenttests.exptests import (
    ExperimentTest,
    ExpTestResult,
    TestStatus,
)
from niceml.utilities.ioutils import read_yaml

operator_dict = {
    "=": operator_module.eq,
    "==": operator_module.eq,
    ">=": operator_module.ge,
    ">": operator_module.gt,
    "<=": operator_module.le,
    "<": operator_module.lt,
}


class MetricCheck(ExperimentTest):
    def __init__(
        self, file: str, operator: str, value: float, value_key: Union[str, List[str]]
    ):
        self.file = file
        self.operator = operator
        self.value = value
        self.value_key = value_key if type(value_key) == list else [value_key]

    def __call__(
        self, experiment_path: str, file_system: Optional[AbstractFileSystem] = None
    ) -> ExpTestResult:
        file_system = file_system or LocalFileSystem()
        yaml_data = read_yaml(join(experiment_path, self.file), file_system)
        for key in self.value_key:
            yaml_data = yaml_data[key]

        operator = operator_dict[self.operator]
        res = operator(yaml_data, self.value)
        name = (
            f"MetricCheck - {self.file} - "
            f"{self.operator} {self.value} - {self.value_key}"
        )
        message = f"Value was extracted with: {yaml_data:0.4f}"
        if res:
            status = TestStatus.OK
        else:
            status = TestStatus.FAILED

        return ExpTestResult(status, name, message)
