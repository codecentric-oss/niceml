from dagster import graph

from niceml.cli.clicommands import train
from niceml.dagster.ops.analysis import analysis
from niceml.dagster.ops.experiment import experiment
from niceml.dagster.ops.exptests import exptests
from niceml.dagster.ops.filelockops import acquire_locks, release_locks
from niceml.dagster.ops.prediction import prediction


# @job(
#    config=cls_run_config,
#    resource_defs={"mlflow": mlflow_tracking},
# )


@graph
def graph_train():
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
