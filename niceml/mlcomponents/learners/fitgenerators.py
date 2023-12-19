"""Module for fit generator"""
from niceml.config.trainparams import TrainParams
from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.mlcomponents.learners.learner import Learner
from niceml.mlcomponents.models.modelfactory import ModelFactory


def fit_generator(  # noqa: PLR0913
    exp_context: ExperimentContext,
    learner: Learner,
    model: ModelFactory,
    train_set,
    validation_set,
    train_params: TrainParams,
    data_description: DataDescription,
):
    """Function to fit the generator with the learner"""
    if train_params.validation_steps is not None:
        print(f"Validation steps: {train_params.validation_steps}")
    if train_params.steps_per_epoch is not None:
        print(f"Steps per epoch: {train_params.steps_per_epoch}")

    learner.run_training(
        exp_context,
        model,
        train_set,
        validation_set,
        train_params,
        data_description,
    )
