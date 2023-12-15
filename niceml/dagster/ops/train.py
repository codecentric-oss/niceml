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
    train_params: TrainParams = Field(default_factory=TrainParams)
    model: dict = create_hydra_init_field(ModelFactory)
    data_description: dict = create_hydra_init_field(DataDescription)
    data_train: dict = create_hydra_init_field(Dataset)
    data_validation: dict = create_hydra_init_field(Dataset)
    model_load_custom_objects: dict = create_hydra_init_field(ModelCustomLoadObjects)
    callbacks: dict = create_hydra_init_field(CallbackInitializer)
    learner: dict = create_hydra_init_field(Learner)
    exp_initializer: dict = create_hydra_init_field(ExpOutInitializer)
    remove_key_list: List[str] = Field(
        default=DEFAULT_REMOVE_CONFIG_KEYS,
        description="These keys are removed from any config recursively before it is saved.",
    )  # TODO: refactor

    @property
    def model_factory_init(self) -> ModelFactory:
        return instantiate(self.model, _convert_=ConvertMode.ALL)

    @property
    def data_description_init(self) -> DataDescription:
        return instantiate(self.data_description, _convert_=ConvertMode.ALL)

    @property
    def data_train_init(self) -> Dataset:
        return instantiate(self.data_train, _convert_=ConvertMode.ALL)

    @property
    def data_validation_init(self) -> Dataset:
        return instantiate(self.data_validation, _convert_=ConvertMode.ALL)

    @property
    def model_load_custom_objects_init(self) -> ModelCustomLoadObjects:
        return instantiate(self.model_load_custom_objects, _convert_=ConvertMode.ALL)

    @property
    def callbacks_init(self) -> CallbackInitializer:
        return instantiate(self.callbacks, _convert_=ConvertMode.ALL)

    @property
    def learner_init(self) -> Learner:
        return instantiate(self.learner, _convert_=ConvertMode.ALL)

    @property
    def exp_initializer_init(self) -> ExpOutInitializer:
        return instantiate(self.exp_initializer, _convert_=ConvertMode.ALL)


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

    config.data_train_init.initialize(config.data_description_init, exp_context)
    config.data_validation_init.initialize(config.data_description_init, exp_context)

    save_exp_data_stats(
        config.data_train_init, exp_context, ExperimentFilenames.STATS_TRAIN
    )
    save_exp_data_stats(
        config.data_validation_init, exp_context, ExperimentFilenames.STATS_TRAIN
    )

    config.exp_initializer_init(exp_context)

    fit_generator(
        exp_context,
        config.learner_init,
        config.model_factory_init,
        config.data_train_init,
        config.data_validation_init,
        config.train_params,
        config.data_description_init,
        config.model_load_custom_objects_init,
        config.callbacks_init(exp_context),
    )
    return exp_context, filelock_dict
