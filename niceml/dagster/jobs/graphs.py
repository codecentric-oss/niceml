"""module for defining the graphs for the dagster jobs"""
from dagster import graph

from niceml.cli.clicommands import train
from niceml.dagster.ops.analysis import analysis
from niceml.dagster.ops.copyexp import copy_exp
from niceml.dagster.ops.cropnumbers import crop_numbers
from niceml.dagster.ops.datageneration import data_generation
from niceml.dagster.ops.dfnormalization import df_normalization
from niceml.dagster.ops.evalcopyexp import eval_copy_exp
from niceml.dagster.ops.experiment import experiment
from niceml.dagster.ops.exptests import exptests
from niceml.dagster.ops.filelockops import acquire_locks, release_locks, clear_locks
from niceml.dagster.ops.imagetotable import image_to_tabular_data
from niceml.dagster.ops.localizeexperiment import localize_experiment
from niceml.dagster.ops.prediction import prediction
from niceml.dagster.ops.splitdata import split_data


@graph
def graph_data_generation():
    """Graph for data generation"""

    current_data_location = data_generation()
    current_data_location = split_data(current_data_location)
    current_data_location = crop_numbers(current_data_location)
    current_data_location = image_to_tabular_data(current_data_location)
    df_normalization(current_data_location)


@graph
def graph_train():
    """Graph for training an experiment"""
    filelock_dict = acquire_locks()
    exp_context = experiment()
    exp_context, filelock_dict = train(exp_context, filelock_dict)
    exp_context, datasets, filelock_dict = prediction(exp_context, filelock_dict)
    exp_context, filelock_dict = analysis(exp_context, datasets, filelock_dict)
    release_locks(filelock_dict)
    exptests(exp_context)


@graph
def graph_eval():
    """Graph for evaluating experiment"""
    filelock_dict = acquire_locks()
    exp_context = localize_experiment()
    exp_context = eval_copy_exp(exp_context)
    exp_context, datasets, filelock_dict = prediction(exp_context, filelock_dict)
    exp_context, filelock_dict = analysis(exp_context, datasets, filelock_dict)
    release_locks(filelock_dict)
    exptests(exp_context)


@graph
def graph_copy_exp():
    """Graph for copy an experiment from one location to another"""
    copy_exp()


@graph
def graph_clearlocks():
    """Clear locks from given lock entries"""
    clear_locks()
