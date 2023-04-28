"""Module for dagster op `localize experiment`"""
import json
from os.path import join

from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.experimenterrors import EmptyExperimentError
from niceml.experiments.experimentinfo import ExperimentInfo, load_exp_info
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.experiments.exppathfinder import get_exp_filepath
from niceml.utilities.fsspec.locationutils import join_location_w_path, open_location
from dagster import Field, Noneable, OpExecutionContext, op


# pylint: disable=use-dict-literal
@op(
    config_schema=dict(
        existing_experiment=Field(
            str,
            description="Used to define the experiment id. "
            "This is an alpha numeric str with the lenth of 4",
        ),
        exp_out_location=Field(
            dict,
            default_value=dict(uri="experiments"),
            description="Folder to store the experiments",
        ),
        exp_folder_pattern=Field(
            Noneable(str),
            default_value=None,
            description="Unused. Only required due to easier configuration",
        ),
    )
)
def localize_experiment(context: OpExecutionContext) -> ExperimentContext:
    """This op localizes the experiment and returns the experiment context"""
    op_config = json.loads(json.dumps(context.op_config))
    exp_out_location: dict = op_config["exp_out_location"]

    exp_path = get_exp_filepath(exp_out_location, op_config["existing_experiment"])
    try:
        with open_location(exp_out_location) as (cur_fs, root_path):
            experiment_info: ExperimentInfo = load_exp_info(
                join(root_path, exp_path, ExperimentFilenames.EXP_INFO),
                cur_fs,
            )
    except FileNotFoundError as error:
        raise EmptyExperimentError(
            f"Experiment {exp_path} has no valid project file."
        ) from error
    local_run_id = experiment_info.run_id
    local_short_id = experiment_info.short_id
    exp_location = join_location_w_path(exp_out_location, exp_path)
    return ExperimentContext(
        fs_config=exp_location, run_id=local_run_id, short_id=local_short_id
    )
