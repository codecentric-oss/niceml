"""Module containing dagster op which copies experiments for the evaluation pipeline"""
import json
import logging
from os.path import join

import yaml
from fsspec import AbstractFileSystem
from tqdm import tqdm

from niceml.config.envconfig import DESCRIPTION_KEY, RUN_ID_KEY, SHORT_ID_KEY
from niceml.dagster.ops.experiment import create_exp_settings
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import ExperimentFilenames, ExpEvalCopyNames
from niceml.utilities.fsspec.locationutils import join_location_w_path, open_location
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
        description=Field(
            str,
            default_value="",
            description="Description of the experiment. Replaces the training description",
        ),
    )
)
def eval_copy_exp(  # pylint: disable=too-many-locals
    context: OpExecutionContext, exp_context: ExperimentContext
):
    """Copy experiment from one to another."""
    op_config = json.loads(json.dumps(context.op_config))
    description: str = op_config["description"]
    exp_folder_pattern: str = op_config["exp_folder_pattern"]
    exp_out_location: dict = op_config["exp_out_location"]
    exp_folder, local_run_id, local_short_id = create_exp_settings(exp_folder_pattern)
    new_exp_location = join_location_w_path(exp_out_location, exp_folder)

    with open_location(exp_context.fs_config) as (
        src_exp_fs,
        src_exp_path,
    ), open_location(new_exp_location) as (target_exp_fs, target_exp_path):
        in_mapper = src_exp_fs.get_mapper(src_exp_path)

        out_mapper = target_exp_fs.get_mapper(target_exp_path)
        logging.getLogger(__name__).info("Starting to copy experiment data")
        eval_copy_exp_names = ExpEvalCopyNames()
        for key in tqdm(in_mapper):
            if key in eval_copy_exp_names:
                out_mapper[key] = in_mapper[key]

        change_ids_from_expinfo(
            target_exp_fs,
            join(target_exp_path, ExperimentFilenames.EXP_INFO),
            local_run_id,
            local_short_id,
            description,
        )

    return ExperimentContext(
        new_exp_location, run_id=local_run_id, short_id=local_short_id
    )


def change_ids_from_expinfo(
    file_system: AbstractFileSystem,
    exp_info_path: str,
    run_id: str,
    short_id: str,
    description: str,
):
    """Changes the run and short_id in an experiment info file"""
    with file_system.open(exp_info_path, "r") as cur_file:
        data = yaml.load(cur_file, Loader=yaml.SafeLoader)

    data[RUN_ID_KEY] = run_id
    data[SHORT_ID_KEY] = short_id
    data[DESCRIPTION_KEY] = (
        description
        if len(description) > 0
        else f"TrainDescription: {data[DESCRIPTION_KEY]}"
    )

    with file_system.open(exp_info_path, "w") as cur_file:
        yaml.dump(data, cur_file, Dumper=yaml.SafeDumper)
