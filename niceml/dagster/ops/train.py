"""Module for train op"""
import json
from typing import Dict, Tuple

from hydra.utils import ConvertMode, instantiate

from niceml.config.hydra import HydraInitField
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
from dagster import OpExecutionContext, op, Out

from niceml.utilities.readwritelock import FileLock

train_config: dict = dict(
    train_params=HydraInitField(TrainParams),
    model=HydraInitField(ModelFactory),
    data_description=HydraInitField(DataDescription),
    data_train=HydraInitField(Dataset),
    data_validation=HydraInitField(Dataset),
    model_load_custom_objects=HydraInitField(ModelCustomLoadObjects),
    callbacks=HydraInitField(CallbackInitializer),
    learner=HydraInitField(Learner),
    exp_initializer=HydraInitField(ExpOutInitializer),
)


@op(config_schema=train_config, out={"expcontext": Out(), "filelock_dict": Out()})
def train(
    context: OpExecutionContext,
    exp_context: ExperimentContext,
    filelock_dict: Dict[str, FileLock],
) -> Tuple[ExperimentContext, Dict[str, FileLock]]:
    """DagsterOp that trains the model"""
    op_config = json.loads(json.dumps(context.op_config))
    write_op_config(op_config, exp_context, OpNames.OP_TRAIN.value)
    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)

    data_train = instantiated_op_config["data_train"]
    data_valid = instantiated_op_config["data_validation"]
    data_description = instantiated_op_config["data_description"]
    custom_model_load_objects = instantiated_op_config["model_load_custom_objects"]

    data_train.initialize(data_description, exp_context)
    data_valid.initialize(data_description, exp_context)

    save_exp_data_stats(data_train, exp_context, ExperimentFilenames.STATS_TRAIN)
    save_exp_data_stats(data_valid, exp_context, ExperimentFilenames.STATS_TRAIN)

    instantiated_op_config["exp_initializer"](exp_context)
    callbacks = instantiated_op_config["callbacks"](exp_context)

    fit_generator(
        exp_context,
        instantiated_op_config["learner"],
        instantiated_op_config["model"],
        data_train,
        data_valid,
        instantiated_op_config["train_params"],
        data_description,
        custom_model_load_objects,
        callbacks,
    )
    return exp_context, filelock_dict
