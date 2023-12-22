from typing import List

from niceml.config.hydra import InitConfig
from niceml.dagster.ops.exptests import ExpTestsConfig
from niceml.experiments.experimenttests.checkfilesfolderstest import (
    CheckFilesFoldersTest,
)
from niceml.experiments.experimenttests.validateexps import (
    ModelsSavedExpTest,
    ParqFilesNoNoneExpTest,
    ExpEmptyTest,
)


class ConfModelsSavedExpTest(InitConfig):
    """Config for ModelsSavedExpTest"""

    target: str = InitConfig.create_target_field(ModelsSavedExpTest)


class ConfParqFilesNoNoneExpTest(InitConfig):
    """Config for ParqFilesNoNoneExpTest"""

    target: str = InitConfig.create_target_field(ParqFilesNoNoneExpTest)


class ConfExpEmptyTest(InitConfig):
    """Config for ExpEmptyTest"""

    target: str = InitConfig.create_target_field(ExpEmptyTest)


class ConfCheckFilesFoldersTest(InitConfig):
    """Config for CheckFilesFoldersTest"""

    target: str = InitConfig.create_target_field(CheckFilesFoldersTest)
    folders: List[str] = ["configs"]
    files: List[str] = [
        "configs/train/model_load_custom_objects.yaml",
        "configs/train/data_description.yaml",
        "train_logs.csv",
    ]


default_test_list = [
    ConfModelsSavedExpTest(),
    ConfParqFilesNoNoneExpTest(),
    ConfExpEmptyTest(),
    ConfCheckFilesFoldersTest(),
]


class ConfExpTestsDefault(ExpTestsConfig):
    """Config for ExpTests"""

    tests_: List[InitConfig] = default_test_list
