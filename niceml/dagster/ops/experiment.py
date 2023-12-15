"""Module for experiment op"""

import mlflow
from pydantic import Field

from niceml.experiments.experimentcontext import ExperimentContext
from niceml.utilities.factoryutils import subs_path_and_create_folder
from niceml.utilities.fsspec.locationutils import join_location_w_path
from niceml.utilities.idutils import generate_short_id
from niceml.utilities.timeutils import generate_timestamp
from dagster import OpExecutionContext, op, Config


class ExperimentConfig(Config):
    exp_out_location: dict = Field(  # TODO: add LocationConfigConfig / Location
        default=dict(uri="experiments"),
        description="Folder to store the experiments",
    )
    exp_folder_pattern: str = Field(
        default="EXP-$RUN_ID-id_$SHORT_ID",
        description="Folder pattern of the experiment. "
        "Can use $RUN_ID and $SHORT_ID to make the name unique",
    )


# pylint: disable=use-dict-literal
@op(
    required_resource_keys={"mlflow"},
)
def experiment(
    context: OpExecutionContext, config: ExperimentConfig
) -> ExperimentContext:
    """This Op creates the experiment params"""
    exp_folder, local_run_id, local_short_id = create_exp_settings(
        config.exp_folder_pattern
    )
    exp_location = join_location_w_path(config.exp_out_location, exp_folder)
    exp_context = ExperimentContext(
        fs_config=exp_location,
        run_id=local_run_id,
        short_id=local_short_id,
    )
    mlflow.set_tags(dict(run_id=local_run_id, short_id=local_short_id))
    mlflow.set_tag("mlflow.runName", local_short_id)

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
