# belongs in the same folder as the yaml file
# QUEST: still used?
from typing import List

import pytest
import yaml
from hydra.utils import instantiate

from niceml.experiments.experimenttests.exptests import (
    ExperimentTest,
    ExpTestResult,
    TestStatus,
)


def pytest_collect_file(parent, path):
    if path.basename.startswith("test") and path.ext in [".yml", ".yaml"]:
        return ExptestYamlCollector.from_parent(parent, fspath=path)


class ExptestYamlCollector(pytest.File):
    def collect(self):
        raw = yaml.safe_load(self.fspath.open())
        # TODO probably yaml path not valid
        test_dict_list = raw["tests"]["test_list"]
        test_obj_list: List[ExperimentTest] = instantiate(test_dict_list)
        for idx, test_obj in enumerate(test_obj_list):
            yield ExptestPytestWrapper.from_parent(
                self,
                name=test_obj.get_test_name(),
                exp_test=test_obj,
                target_path=self.fspath.dirname,
                index=idx,
            )


class ExptestPytestWrapper(pytest.Item):
    def __init__(
        self, name, parent, exp_test: ExperimentTest, target_path: str, index: int
    ):
        super().__init__(name, parent)
        self.exp_test = exp_test
        self.target_path = target_path
        self.index = index

    def runtest(self):
        ret_val: ExpTestResult = self.exp_test(self.target_path)
        if ret_val.status == TestStatus.FAILED:
            raise ExptestPytestError(self, ret_val)

    def repr_failure(
        self,
        excinfo,
        style=None,
    ):
        """Called when self.runtest() raises an exception."""
        if isinstance(excinfo.value, ExptestPytestError):
            exp_test_result: ExpTestResult
            _, exp_test_result = excinfo.value.args
            return str(exp_test_result)

    def reportinfo(self):
        return self.fspath, self.index, f"usecase: {self.name}"


class ExptestPytestError(Exception):
    """Custom exception for error reporting."""
