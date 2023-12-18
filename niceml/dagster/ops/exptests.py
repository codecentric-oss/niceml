"""Module for exptests"""
from typing import List

from dagster import OpExecutionContext, op, Config
from hydra.utils import ConvertMode, instantiate
from pydantic import Field

from niceml.config.defaultremoveconfigkeys import DEFAULT_REMOVE_CONFIG_KEYS
from niceml.config.hydra import create_hydra_init_field
from niceml.config.writeopconfig import write_op_config
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.experimenttests.testinitializer import ExpTestProcess
from niceml.experiments.expfilenames import OpNames
from niceml.utilities.fsspec.locationutils import open_location


class ExpTestsConfig(Config):
    tests_: dict = create_hydra_init_field(target_class=ExpTestProcess, alias="tests")
    remove_key_list: List[str] = Field(
        default=DEFAULT_REMOVE_CONFIG_KEYS,
        description="These key are removed from any config recursively before it is saved.",
    )

    @property
    def tests(self) -> ExpTestProcess:
        return instantiate(self.tests_, _convert_=ConvertMode.ALL)


# pylint: disable=use-dict-literal
@op(
    required_resource_keys={"mlflow"},
)
def exptests(
    context: OpExecutionContext, exp_context: ExperimentContext, config: ExpTestsConfig
) -> ExperimentContext:
    """op to run the experiment tests"""
    write_op_config(
        config, exp_context, OpNames.OP_EXPTESTS.value, config.remove_key_list
    )
    exp_test_process = config.tests
    with open_location(exp_context.fs_config) as (file_system, root_path):
        exp_test_process(root_path, file_system=file_system)
    return exp_context
