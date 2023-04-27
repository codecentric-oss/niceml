"""Module for experiment op"""
import json

from niceml.config.writeopconfig import write_op_config
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import OpNames
from niceml.utilities.factoryutils import subs_path_and_create_folder
from niceml.utilities.fsspec.locationutils import join_location_w_path
from niceml.utilities.idutils import generate_short_id
from niceml.utilities.timeutils import generate_timestamp
from dagster import Field, OpExecutionContext, op


# pylint: disable=use-dict-literal
@op(
    config_schema=dict(
        exp_out_location=Field(
            dict,
            default_value=dict(uri="experiments"),
            description="Folder to store the experiments",
        ),
        exp_folder_pattern=Field(
            str,
            default_value="EXP-$RUN_ID-id_$SHORT_ID",
            description="Folder pattern of the experiment. "
            "Can use $RUN_ID and $SHORT_ID to make the name unique",
        ),
    )
)
def experiment(context: OpExecutionContext) -> ExperimentContext:
    """This Op creates the experiment params"""
    op_config = json.loads(json.dumps(context.op_config))
    exp_out_location: dict = op_config["exp_out_location"]
    exp_folder_pattern: str = op_config["exp_folder_pattern"]
    exp_folder, local_run_id, local_short_id = create_exp_settings(exp_folder_pattern)
    exp_location = join_location_w_path(exp_out_location, exp_folder)
    exp_context = ExperimentContext(
        fs_config=exp_location,
        run_id=local_run_id,
        short_id=local_short_id,
    )
    write_op_config(op_config, exp_context, OpNames.OP_EXPERIMENT.value)

    return exp_context


def create_exp_settings(exp_folder_pattern):
    """Creates the experiment settings"""
    local_run_id = generate_timestamp()
    local_short_id = generate_short_id(local_run_id)
    exp_folder = subs_path_and_create_folder(
        exp_folder_pattern,
        local_short_id,
        local_run_id,
    )
    return exp_folder, local_run_id, local_short_id
