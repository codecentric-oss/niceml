"""Module for dagster op `localize experiment`"""
import json

from dagster import Field, Noneable, OpExecutionContext, op

from niceml.experiments.experimentcontext import (
    ExperimentContext,
    get_experiment_context,
)


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
    return get_experiment_context(exp_out_location, op_config["existing_experiment"])
