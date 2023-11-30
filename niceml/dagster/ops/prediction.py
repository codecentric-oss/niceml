"""Module for prediction op"""
import json
from os.path import join
from typing import Dict, Optional, Tuple

import numpy as np
import tqdm
from dagster import Field, Noneable, OpExecutionContext, op, Out
from hydra.utils import ConvertMode, instantiate

from niceml.config.defaultremoveconfigkeys import DEFAULT_REMOVE_CONFIG_KEYS
from niceml.config.hydra import HydraInitField, HydraMapField
from niceml.config.writeopconfig import write_op_config
from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datasets.dataset import Dataset
from niceml.experiments.expdatalocalstorageloader import create_expdata_from_expcontext
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.expfilenames import ExperimentFilenames, OpNames
from niceml.mlcomponents.modelloader.modelloader import ModelLoader
from niceml.mlcomponents.predictionfunction.predictionfunction import PredictionFunction
from niceml.mlcomponents.predictionhandlers.predictionhandler import PredictionHandler
from niceml.utilities.fsspec.locationutils import join_fs_path, open_location
from niceml.utilities.readwritelock import FileLock


# pylint: disable=use-dict-literal
@op(
    config_schema=dict(
        prediction_handler=HydraInitField(PredictionHandler),
        datasets=HydraMapField(Dataset),
        prediction_steps=Field(
            Noneable(int),
            default_value=None,
            description="If None the whole datasets are processed. "
            "Otherwise only `prediction_steps` are evaluated.",
        ),
        model_loader=HydraInitField(ModelLoader),
        prediction_function=HydraInitField(PredictionFunction),
        remove_key_list=Field(
            list,
            default_value=DEFAULT_REMOVE_CONFIG_KEYS,
            description="These key are removed from any config recursively before it is saved.",
        ),
    ),
    out={"expcontext": Out(), "datasets": Out(), "filelock_dict": Out()},
    required_resource_keys={"mlflow"},
)
def prediction(
    context: OpExecutionContext,
    exp_context: ExperimentContext,
    filelock_dict: Dict[str, FileLock],
) -> Tuple[ExperimentContext, Dict[str, Dataset], Dict[str, FileLock]]:
    """Dagster op to predict the stored model with the given datasets"""
    op_config = json.loads(json.dumps(context.op_config))
    write_op_config(
        op_config,
        exp_context,
        OpNames.OP_PREDICTION.value,
        op_config["remove_key_list"],
    )
    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)
    data_description: DataDescription = (
        exp_context.instantiate_datadescription_from_yaml()
    )

    exp_data: ExperimentData = create_expdata_from_expcontext(exp_context)
    model_path: str = exp_data.get_model_path(relative_path=True)
    model_loader: ModelLoader = instantiated_op_config["model_loader"]
    with open_location(exp_context.fs_config) as (exp_fs, exp_root):
        model = model_loader(
            join_fs_path(exp_fs, exp_root, model_path),
            file_system=exp_fs,
        )

    datasets_dict: Dict[str, Dataset] = instantiated_op_config["datasets"]

    for dataset_key, cur_pred_set in datasets_dict.items():
        context.log.info(f"Predict dataset: {dataset_key}")
        cur_pred_set.initialize(data_description, exp_context)
        save_exp_data_stats(cur_pred_set, exp_context, ExperimentFilenames.STATS_PRED)
        predict_dataset(
            data_description=data_description,
            prediction_steps=instantiated_op_config["prediction_steps"],
            model=model,
            prediction_set=cur_pred_set,
            prediction_handler=instantiated_op_config["prediction_handler"],
            exp_context=exp_context,
            filename=dataset_key,
            prediction_function=instantiated_op_config["prediction_function"],
        )

    return exp_context, datasets_dict, filelock_dict


def predict_dataset(  # noqa: PLR0913
    data_description: DataDescription,
    model,
    prediction_handler: PredictionHandler,
    prediction_set: Dataset,
    filename: str,
    exp_context: ExperimentContext,
    prediction_function: PredictionFunction,
    prediction_steps: Optional[int] = None,
):
    """Predicts the given dataset with the given model and prediction handler"""
    batch_count: int = len(prediction_set)
    batch_count = (
        batch_count if prediction_steps is None else min(batch_count, prediction_steps)
    )
    progress = tqdm.tqdm(total=batch_count)
    prediction_handler.set_params(exp_context, filename, data_description)
    prediction_handler.initialize()
    with prediction_handler as handler:
        for index, (data_info, batch) in enumerate(prediction_set.iter_with_info()):
            data_x, _ = batch
            pred = prediction_function.predict(model, data_x)
            handler.add_prediction(data_info, pred)
            progress.update()
            if index >= batch_count:
                progress.close()
                break


def is_numpy_output(output) -> bool:
    """Checks if the output of the model is a numpy array"""
    if isinstance(output, np.ndarray):
        return True
    if isinstance(output, list) and isinstance(output[0], np.ndarray):
        return True
    if isinstance(output, dict) and isinstance(
        output[list(output.keys())[0]], np.ndarray
    ):
        return True

    return False


def save_exp_data_stats(
    dataset: Dataset, exp_context: ExperimentContext, output_name: str
):
    """Save the stats of the experiment data to a yaml file"""
    yaml_file = join(ExperimentFilenames.DATASETS_STATS_FOLDER, output_name)
    set_stats: dict = dataset.get_dataset_stats()
    set_name: str = dataset.get_set_name()
    stats_info = {}
    try:
        stats_info = exp_context.read_yaml(yaml_file)
    except FileNotFoundError:
        pass
    stats_info[set_name] = set_stats
    exp_context.write_yaml(stats_info, yaml_file)
