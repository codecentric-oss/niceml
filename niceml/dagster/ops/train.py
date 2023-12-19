"""Module for train op"""
from typing import Dict, Tuple, List

from dagster import OpExecutionContext, op, Out, Config
from hydra.utils import ConvertMode, instantiate
from pydantic import Field

from niceml.config.defaultremoveconfigkeys import DEFAULT_REMOVE_CONFIG_KEYS
from niceml.config.hydra import create_hydra_init_field
from niceml.config.trainparams import TrainParams
from niceml.config.writeopconfig import write_op_config
from niceml.dagster.ops.prediction import save_exp_data_stats
from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import ExperimentFilenames, OpNames
from niceml.experiments.expoutinitializer import ExpOutInitializer
from niceml.mlcomponents.callbacks.callbackinitializer import CallbackInitializer
from niceml.mlcomponents.learners.fitgenerators import fit_generator
from niceml.mlcomponents.learners.learner import Learner
from niceml.mlcomponents.modelcompiler.modelcustomloadobjects import (
    ModelCustomLoadObjects,
)
from niceml.mlcomponents.models.modelfactory import ModelFactory
from niceml.utilities.readwritelock import FileLock


class TrainConfig(Config):
    train_params: TrainParams = Field(
        default_factory=TrainParams,
    )
    model_field: dict = create_hydra_init_field(
        target_class=ModelFactory, alias="model"
    )
    data_description_: dict = create_hydra_init_field(
        target_class=DataDescription, alias="data_description"
    )
    data_train_: dict = create_hydra_init_field(
        target_class=Dataset, alias="data_train"
    )
    data_validation_: dict = create_hydra_init_field(
        target_class=Dataset, alias="data_validation"
    )
    model_load_custom_objects_: dict = create_hydra_init_field(
        target_class=ModelCustomLoadObjects, alias="model_load_custom_objects"
    )
    callbacks_: dict = create_hydra_init_field(
        target_class=CallbackInitializer, alias="callbacks"
    )
    learner_: dict = create_hydra_init_field(target_class=Learner, alias="learner")
    exp_initializer_: dict = create_hydra_init_field(
        target_class=ExpOutInitializer, alias="exp_initializer"
    )
    remove_key_list: List[str] = Field(
        default=DEFAULT_REMOVE_CONFIG_KEYS,
        description="These keys are removed from any config recursively before it is saved.",
    )  # TODO: refactor

    @property
    def model_factory(self) -> ModelFactory:
        return instantiate(self.model_field, _convert_=ConvertMode.ALL)

    @property
    def data_description(self) -> DataDescription:
        return instantiate(self.data_description_, _convert_=ConvertMode.ALL)

    @property
    def data_train(self) -> Dataset:
        return instantiate(self.data_train_, _convert_=ConvertMode.ALL)

    @property
    def data_validation(self) -> Dataset:
        return instantiate(self.data_validation_, _convert_=ConvertMode.ALL)

    @property
    def model_load_custom_objects(self) -> ModelCustomLoadObjects:
        return instantiate(self.model_load_custom_objects_, _convert_=ConvertMode.ALL)

    @property
    def callbacks(self) -> CallbackInitializer:
        return instantiate(self.callbacks_, _convert_=ConvertMode.ALL)

    @property
    def learner(self) -> Learner:
        return instantiate(self.learner_, _convert_=ConvertMode.ALL)

    @property
    def exp_initializer(self) -> ExpOutInitializer:
        return instantiate(self.exp_initializer_, _convert_=ConvertMode.ALL)


@op(
    out={"expcontext": Out(), "filelock_dict": Out()},
    required_resource_keys={"mlflow"},
)
def train(
    context: OpExecutionContext,
    exp_context: ExperimentContext,
    filelock_dict: Dict[str, FileLock],
    config: TrainConfig,
) -> Tuple[ExperimentContext, Dict[str, FileLock]]:
    """DagsterOp that trains the model"""
    write_op_config(config, exp_context, OpNames.OP_TRAIN.value, config.remove_key_list)
    config.data_train.initialize(config.data_description, exp_context)
    config.data_validation.initialize(config.data_description, exp_context)
    save_exp_data_stats(config.data_train, exp_context, ExperimentFilenames.STATS_TRAIN)
    save_exp_data_stats(
        config.data_validation, exp_context, ExperimentFilenames.STATS_TRAIN
    )

    config.exp_initializer(exp_context)

    fit_generator(
        exp_context,
        config.learner,
        config.model_factory,
        config.data_train,
        config.data_validation,
        config.train_params,
        config.data_description,
        config.model_load_custom_objects,
        config.callbacks(exp_context),
    )
    return exp_context, filelock_dict
