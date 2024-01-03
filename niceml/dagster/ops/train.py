"""Module for train op"""
from typing import Dict, Tuple, List

from dagster import OpExecutionContext, op, Out
from pydantic import Field

from niceml.config.defaultremoveconfigkeys import DEFAULT_REMOVE_CONFIG_KEYS
from niceml.config.config import InitConfig, Config
from niceml.config.trainparams import TrainParams
from niceml.config.writeopconfig import write_op_config
from niceml.dagster.ops.prediction import save_exp_data_stats
from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import ExperimentFilenames, OpNames
from niceml.experiments.expoutinitializer import ExpOutInitializer
from niceml.mlcomponents.learners.fitgenerators import fit_generator
from niceml.mlcomponents.learners.learner import Learner
from niceml.mlcomponents.models.modelfactory import ModelFactory
from niceml.utilities.readwritelock import FileLock


class TrainConfig(Config):
    train_params: TrainParams = Field(
        default_factory=TrainParams,
    )
    model_factory: InitConfig = InitConfig.create_config_field(
        target_class=ModelFactory
    )
    data_description: InitConfig = InitConfig.create_config_field(
        target_class=DataDescription,
    )
    data_train: InitConfig = InitConfig.create_config_field(target_class=Dataset)
    data_validation: InitConfig = InitConfig.create_config_field(target_class=Dataset)
    learner: InitConfig = InitConfig.create_config_field(target_class=Learner)
    exp_initializer: InitConfig = InitConfig.create_config_field(
        target_class=ExpOutInitializer
    )
    remove_key_list: List[str] = Field(
        default=DEFAULT_REMOVE_CONFIG_KEYS,
        description="These keys are removed from any config recursively before it is saved.",
    )  # TODO: refactor


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
    data_train = config.data_train.instantiate()
    data_validation = config.data_validation.instantiate()
    data_train.initialize(config.data_description, exp_context)
    data_validation.initialize(config.data_description, exp_context)
    save_exp_data_stats(data_train, exp_context, ExperimentFilenames.STATS_TRAIN)
    save_exp_data_stats(data_validation, exp_context, ExperimentFilenames.STATS_TRAIN)

    exp_initializer: ExpOutInitializer = config.exp_initializer.instantiate()
    exp_initializer(exp_context)

    fit_generator(
        exp_context,
        config.learner.instantiate(),
        config.model_factory.instantiate(),
        data_train,
        data_validation,
        config.train_params,
        config.data_description.instantiate(),
    )
    return exp_context, filelock_dict
