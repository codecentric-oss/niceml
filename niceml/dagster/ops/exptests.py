"""Module for exptests"""
import json

from hydra.utils import ConvertMode, instantiate

from niceml.config.defaultremoveconfigkeys import DEFAULT_REMOVE_CONFIG_KEYS
from niceml.config.hydra import HydraInitField
from niceml.config.writeopconfig import write_op_config
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.experimenttests.testinitializer import ExpTestProcess
from niceml.experiments.expfilenames import OpNames
from niceml.utilities.fsspec.locationutils import open_location
from dagster import OpExecutionContext, op, Field


# pylint: disable=use-dict-literal
@op(
    config_schema=dict(
        tests=HydraInitField(ExpTestProcess),
        remove_key_list=Field(
            list,
            default_value=DEFAULT_REMOVE_CONFIG_KEYS,
            description="These key are removed from any config recursively before it is saved.",
        ),
    ),
    required_resource_keys={"mlflow"},
)
def exptests(
    context: OpExecutionContext, exp_context: ExperimentContext
) -> ExperimentContext:
    """op to run the experiment tests"""
    op_config = json.loads(json.dumps(context.op_config))
    write_op_config(
        op_config, exp_context, OpNames.OP_EXPTESTS.value, op_config["remove_key_list"]
    )
    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)
    exp_test_process: ExpTestProcess = instantiated_op_config["tests"]
    with open_location(exp_context.fs_config) as (file_system, root_path):
        exp_test_process(root_path, file_system=file_system)
    return exp_context
