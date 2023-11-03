"""Module containing all dagster jobs"""
from dagster_mlflow import mlflow_tracking

from niceml.config.hydra import hydra_conf_mapping_factory
from niceml.dagster.ops.analysis import analysis
from niceml.dagster.ops.copyexp import copy_exp
from niceml.dagster.ops.cropnumbers import crop_numbers
from niceml.dagster.ops.datageneration import data_generation
from niceml.dagster.ops.dfnormalization import df_normalization
from niceml.dagster.ops.evalcopyexp import eval_copy_exp
from niceml.dagster.ops.experiment import experiment
from niceml.dagster.ops.exptests import exptests
from niceml.dagster.ops.filelockops import clear_locks, acquire_locks, release_locks
from niceml.dagster.ops.imagetotable import image_to_tabular_data
from niceml.dagster.ops.localizeexperiment import localize_experiment
from niceml.dagster.ops.prediction import prediction
from niceml.dagster.ops.splitdata import split_data
from niceml.dagster.ops.train import train
from niceml.dagster.resources.locations import locations_resource
from dagster import job


@job(config=hydra_conf_mapping_factory())
def job_data_generation():
    """Job for data generation"""

    current_data_location = data_generation()  # pylint: disable=no-value-for-parameter
    current_data_location = split_data(
        current_data_location
    )  # pylint: disable=no-value-for-parameter
    current_data_location = crop_numbers(
        current_data_location
    )  # pylint: disable=no-value-for-parameter
    current_data_location = image_to_tabular_data(current_data_location)
    df_normalization(current_data_location)


@job(config=hydra_conf_mapping_factory(), resource_defs={"mlflow": mlflow_tracking})
def job_train():
    """Job for training an experiment"""
    filelock_dict = acquire_locks()  # pylint: disable=no-value-for-parameter
    exp_context = experiment()  # pylint: disable=no-value-for-parameter
    exp_context, filelock_dict = train(
        exp_context, filelock_dict
    )  # pylint: disable=no-value-for-parameter
    exp_context, datasets, filelock_dict = prediction(
        exp_context, filelock_dict
    )  # pylint: disable=no-value-for-parameter
    exp_context, filelock_dict = analysis(
        exp_context, datasets, filelock_dict
    )  # pylint: disable=no-value-for-parameter
    release_locks(filelock_dict)  # pylint: disable=no-value-for-parameter
    exptests(exp_context)  # pylint: disable=no-value-for-parameter


@job(config=hydra_conf_mapping_factory(), resource_defs={"mlflow": mlflow_tracking})
def job_eval():
    """Job for evaluating experiment"""
    filelock_dict = acquire_locks()  # pylint: disable=no-value-for-parameter
    exp_context = localize_experiment()  # pylint: disable=no-value-for-parameter
    exp_context = eval_copy_exp(exp_context)  # pylint: disable=no-value-for-parameter
    exp_context, datasets, filelock_dict = prediction(
        exp_context, filelock_dict
    )  # pylint: disable=no-value-for-parameter
    exp_context, filelock_dict = analysis(
        exp_context, datasets, filelock_dict
    )  # pylint: disable=no-value-for-parameter
    release_locks(filelock_dict)  # pylint: disable=no-value-for-parameter
    exptests(exp_context)  # pylint: disable=no-value-for-parameter


@job(
    config=hydra_conf_mapping_factory(),
    resource_defs={
        "locations": locations_resource,
    },
)
def job_copy_exp():
    """Copy an experiment from one location to another"""
    copy_exp()  # pylint: disable=no-value-for-parameter


@job(
    config=hydra_conf_mapping_factory(),
)
def job_clearlocks():
    """Clear locks from given lock entries"""
    clear_locks()  # pylint: disable=no-value-for-parameter
