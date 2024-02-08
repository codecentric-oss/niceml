"""Module for exptests"""
from typing import List

from dagster import OpExecutionContext, op
from pydantic import Field
from dagster import Config
from typing_extensions import Annotated

from niceml.config.config import InitConfig
from niceml.config.defaultremoveconfigkeys import DEFAULT_REMOVE_CONFIG_KEYS
from niceml.config.writeopconfig import write_op_config
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.experimenttests.testinitializer import ExpTestProcess
from niceml.experiments.expfilenames import OpNames
from niceml.utilities.fsspec.locationutils import open_location


class ExpTestsConfig(Config):
    exp_test_process: InitConfig = InitConfig.create_config_field(
        target_class=ExpTestProcess
    )

    remove_key_list: List[str] = Field(
        default=DEFAULT_REMOVE_CONFIG_KEYS,
        description="These key are removed from any config recursively before it is saved.",
    )


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
    exp_test_process = config.exp_test_process.instantiate()
    with open_location(exp_context.fs_config) as (file_system, root_path):
        exp_test_process(root_path, file_system=file_system)
    return exp_context
