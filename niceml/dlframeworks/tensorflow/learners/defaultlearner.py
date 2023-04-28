"""Module for default learner"""
import tensorflow as tf

# pylint: disable=import-error, no-name-in-module
from tensorflow.keras.models import Model

from niceml.config.trainparams import TrainParams
from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.mlcomponents.learners.learner import Learner
from niceml.mlcomponents.modelcompiler.modelcompiler import ModelCompiler
from niceml.mlcomponents.modelcompiler.modelcustomloadobjects import (
    ModelCustomLoadObjects,
)
from niceml.mlcomponents.models.modelbundle import ModelBundle
from niceml.mlcomponents.models.modelfactory import ModelFactory


# pylint: disable=too-few-public-methods
class DefaultLearner(Learner):
    """default learner for keras/tensorflow models"""

    def __init__(self, model_compiler: ModelCompiler):
        self.model_compiler: ModelCompiler = model_compiler

    # pylint: disable=too-many-arguments, unused-argument
    def run_training(
        self,
        exp_context: ExperimentContext,
        model_factory: ModelFactory,
        train_set: Dataset,
        validation_set: Dataset,
        train_params: TrainParams,
        data_description: DataDescription,
        custom_load_objects: ModelCustomLoadObjects,
        callbacks: list,
    ):
        model_bundle: ModelBundle = self.model_compiler.compile(
            model_factory, data_description
        )
        initialized_model: Model = model_bundle.model
        train_params: TrainParams
        validation_steps = None
        if train_params.validation_steps is not None:
            validation_steps = min(train_params.validation_steps, len(validation_set))
        steps_per_epoch = None
        if train_params.steps_per_epoch is not None:
            steps_per_epoch = min(train_params.steps_per_epoch, len(train_set))
        with tf.keras.utils.custom_object_scope(custom_load_objects()):
            history = initialized_model.fit(
                train_set,
                epochs=train_params.epochs,
                validation_data=validation_set,
                callbacks=callbacks,
                validation_steps=validation_steps,
                steps_per_epoch=steps_per_epoch,
            )
        return history
