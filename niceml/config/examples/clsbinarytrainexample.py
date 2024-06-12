import os
import re
from collections import defaultdict
from os.path import join
from typing import List, Dict, Any

from dagster import (
    JobDefinition,
    ConfigSchema,
    ConfigMapping,
    Config,
    Field as DagsterField,
)
from dagster import RunConfig, Definitions
from dagster import graph
from dagster_mlflow import mlflow_tracking
from keras.optimizers import Adam
from pydantic import Field

from niceml.config.config import InitConfig, MapInitConfig, get_class_path
from niceml.config.trainparams import TrainParams
from niceml.dagster.ops.analysis import AnalysisConfig
from niceml.dagster.ops.analysis import analysis
from niceml.dagster.ops.experiment import ExperimentConfig
from niceml.dagster.ops.experiment import experiment
from niceml.dagster.ops.exptests import ExpTestsConfig
from niceml.dagster.ops.exptests import exptests
from niceml.dagster.ops.filelockops import LocksConfig
from niceml.dagster.ops.filelockops import acquire_locks, release_locks
from niceml.dagster.ops.prediction import PredictionConfig
from niceml.dagster.ops.prediction import prediction
from niceml.dagster.ops.train import TrainConfig, train
from niceml.data.datadescriptions.clsdatadescription import ClsDataDescription
from niceml.data.datainfolistings.clsdatainfolisting import DirClsDataInfoListing
from niceml.data.dataloaders.clsdataloader import ClsDataLoader
from niceml.dlframeworks.keras.callbacks.callback_factories import (
    InitCallbackFactory,
    LoggingOutputCallbackFactory,
    ModelCallbackFactory,
)
from niceml.dlframeworks.keras.callbacks.nancheckcallback import LossNanCheckCallback
from niceml.dlframeworks.keras.datasets.kerasgenericdataset import KerasGenericDataset
from niceml.dlframeworks.keras.kerasmodelloader import KerasModelLoader
from niceml.dlframeworks.keras.learners.keraslearner import KerasLearner
from niceml.dlframeworks.keras.modelcompiler.defaultmodelcompiler import (
    DefaultModelCompiler,
)
from niceml.dlframeworks.keras.models.mobilenet import OwnMobileNetModel
from niceml.dlframeworks.keras.predictionfunctions.keraspredictionfunction import (
    KerasPredictionFunction,
)
from niceml.experiments.experimenttests.checkfilesfolderstest import (
    CheckFilesFoldersTest,
)
from niceml.experiments.experimenttests.testinitializer import ExpTestProcess
from niceml.experiments.experimenttests.validateexps import (
    ModelsSavedExpTest,
    ParqFilesNoNoneExpTest,
    ExpEmptyTest,
)
from niceml.experiments.expoutinitializer import ExpOutInitializer
from niceml.mlcomponents.callbacks.callbackinitializer import CallbackInitializer
from niceml.mlcomponents.modelcompiler.modelcustomloadobjects import (
    ModelCustomLoadObjects,
)
from niceml.mlcomponents.predictionhandlers.vectorpredictionhandler import (
    VectorPredictionHandler,
)
from niceml.mlcomponents.resultanalyzers.dataframes.clsmetric import ClsMetric
from niceml.mlcomponents.resultanalyzers.dataframes.dfanalyzer import DataframeAnalyzer
from niceml.mlcomponents.targettransformer.imageinputtransformer import (
    ImageInputTransformer,
)
from niceml.mlcomponents.targettransformer.targettransformercls import (
    TargetTransformerClassification,
)
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.readwritelock import FileLock

data_description = ClsDataDescription.create_config(
    classes=["0", "1", "2", "3"],
    target_size=ImageSize.create_config(width=1024, height=1024),
)

dataset_train = KerasGenericDataset.create_config(
    batch_size=16,
    set_name="train",
    shuffle=True,
    datainfo_listing=DirClsDataInfoListing.create_config(
        location=dict(uri=join(os.getenv("DATA_URI"), "numbers_cropped_split")),
        sub_dir="train",
    ),
    data_loader=ClsDataLoader.create_config(data_description=data_description),
    target_transformer=TargetTransformerClassification.create_config(
        data_description=data_description,
    ),
    input_transformer=ImageInputTransformer.create_config(
        data_description=data_description
    ),
    net_data_logger=None,
)

dataset_validation = dataset_train.model_copy(
    update=dict(
        set_name="validation",
        datainfo_listing=dataset_train.datainfo_listing.model_copy(
            update=dict(sub_dir="validation")
        ),
        shuffle=False,
    )
)

dataset_test = dataset_train.model_copy(
    update=dict(
        set_name="test",
        datainfo_listing=dataset_train.datainfo_listing.model_copy(
            update=dict(sub_dir="test")
        ),
        shuffle=False,
    )
)

acquire_locks_config = LocksConfig(file_lock_dict=MapInitConfig.create(FileLock))
experiment_config = ExperimentConfig(
    exp_out_location=dict(uri=os.getenv("EXPERIMENT_URI")),
    exp_folder_pattern="CLS-$RUN_ID-id_$SHORT_ID",
)
train_config = TrainConfig(
    train_params=TrainParams(),
    model_factory=OwnMobileNetModel.create_config(),
    data_description=data_description,
    data_train=dataset_train,
    data_validation=dataset_validation,
    learner=KerasLearner.create_config(
        model_compiler=DefaultModelCompiler.create_config(
            loss="categorical_crossentropy",
            metrics=["accuracy"],
            optimizer=InitConfig.create(Adam, learning_rate=0.0001),
        ),
        callback_initializer=CallbackInitializer.create_config(
            callback_list=[
                InitCallbackFactory.create_config(
                    callback=InitConfig.create(LossNanCheckCallback),
                ),
                InitConfig.create(LoggingOutputCallbackFactory),
            ],
            callback_dict=dict(
                save_model=ModelCallbackFactory.create_config(
                    model_subfolder="models/model-id_{short_id}-ep{epoch:03d}.hdf5"
                )
            ),
        ),
        model_load_custom_objects=ModelCustomLoadObjects.create_config(),
    ),
    exp_initializer=ExpOutInitializer.create_config(
        exp_name="SampleCls", exp_prefix="CLS", git_modules=["niceml"]
    ),
)

prediction_config = PredictionConfig(
    prediction_handler=VectorPredictionHandler.create_config(),
    datasets=MapInitConfig.create(
        map_target_class=KerasGenericDataset,
        test=dataset_test,
        validation=dataset_validation,
        train_eval=dataset_train.model_copy(update=dict(shuffle=False)),
    ),
    model_loader=KerasModelLoader.create_config(),
    prediction_function=KerasPredictionFunction.create_config(),
    prediction_steps=2,
)
analysis_config = AnalysisConfig(
    result_analyzer=DataframeAnalyzer.create_config(
        metrics=[
            ClsMetric.create_config(
                function="accuracy",
                source_col="class_idx",
                target_cols_prefix="pred_",
            ),
            ClsMetric.create_config(
                function="confusion_matrix",
                source_col="class_idx",
                target_cols_prefix="pred_",
            ),
        ]
    ),
)

exptests_config = ExpTestsConfig(
    exp_test_process=ExpTestProcess.create_config(
        test_list=[
            ModelsSavedExpTest.create_config(),
            ParqFilesNoNoneExpTest.create_config(),
            ExpEmptyTest.create_config(),
            CheckFilesFoldersTest.create_config(
                folders=["configs"],
                files=[
                    "configs/train/data_description.yaml",
                    "train_logs.csv",
                    "experiment_info.yaml",
                ],
            ),
        ]
    )
)

cls_run_config = RunConfig(
    ops={
        "acquire_locks": acquire_locks_config,
        "experiment": experiment_config,
        "train": train_config,
        "prediction": prediction_config,
        "analysis": analysis_config,
        "exptests": exptests_config,
    },
    resources={
        "mlflow": {
            "config": {
                "mlflow_tracking_uri": os.getenv("MLFLOW_TRACKING_URI", "mlflow-logs"),
                "experiment_name": "CLS",
            }
        }
    },
)


def build_config_schema(run_config: RunConfig, global_keys: Dict[str, str]) -> dict:
    config_dict = run_config.to_config_dict()
    duplicates = find_identical_entries(config_dict)
    return {}


import hashlib
import json


def calculate_checksum(data):
    """
    Recursively calculate checksum for a hierarchical dictionary.
    """
    # If data is not a dictionary, return its hash directly
    if not isinstance(data, dict):
        return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

    # Sort the dictionary to ensure consistent checksums
    sorted_data = {
        key: calculate_checksum(value) for key, value in sorted(data.items())
    }

    # Use JSON representation for hashing
    checksum = hashlib.md5(json.dumps(sorted_data, sort_keys=True).encode()).hexdigest()
    return checksum


def find_identical_entries(data):
    """
    Find identical entries in the given hierarchical dictionary.
    """
    checksum_dict = {}
    identical_entries = {}

    for key, value in data.items():
        checksum = calculate_checksum(value)
        if checksum in checksum_dict:
            identical_entries.setdefault(checksum, []).append(key)
        else:
            checksum_dict[checksum] = key

    return identical_entries


def build_config(*args, **kwargs) -> RunConfig:
    return RunConfig()


class ConfigMapper:
    def __init__(self, global_keys: Dict[str, List[str]]):
        self.global_keys = global_keys
        self.environment_variable_pattern = r"^\$\{env\(([A-Z_][A-Z0-9_]*)\)\}$"

    def build_config_schema(self, run_config: RunConfig):
        schema = defaultdict(dict)

        for op, config in run_config.ops.items():
            schema["ops"][op] = defaultdict(dict)

            for config_field in config.model_fields_set:
                config_value = getattr(config, config_field)
                if isinstance(config_value, InitConfig):
                    schema["ops"][op][config_field] = DagsterField(
                        dict, default_value=config_value.model_dump(by_alias=True)
                    )
                elif isinstance(config_value, Config):
                    schema["ops"][op][config_field] = config_value.to_fields_dict()
                else:
                    schema["ops"][op][config_field] = DagsterField(
                        type(config_value), default_value=config_value
                    )
            schema["ops"][op] = dict(schema["ops"][op])
        schema["globals"] = defaultdict(dict)
        for gloabals_key, globals_links in self.global_keys.items():
            for global_link in globals_links:
                schema["globals"][gloabals_key] = self._get_value_from_flattened_key(
                    schema, global_link
                )

                self._set_value_from_flattened_key(
                    schema,
                    key=global_link,
                    value=DagsterField(str, default_value=f"$globals.{gloabals_key}"),
                )
        schema = dict(schema)

        schema["resources"] = DagsterField(dict, default_value=run_config.resources)

        return schema

    def map_schema_to_config(self, run_config_dict: dict):
        self._replace_environment_variables(run_config_dict=run_config_dict)
        self._replace_globales(run_config_dict=run_config_dict)
        run_config_dict = self._add_config_level(run_config_dict=run_config_dict)
        return run_config_dict

    def _add_config_level(self, run_config_dict: dict) -> dict:
        ops_config = run_config_dict.pop("ops")
        run_config_dict["ops"] = defaultdict(dict)

        for op_config_key, op_config_value in ops_config.items():
            run_config_dict["ops"][op_config_key] = {"config": op_config_value}
        run_config_dict["ops"] = dict(run_config_dict["ops"])

        return run_config_dict

    def _get_value_from_flattened_key(self, data: dict, key: str):
        keys = key.split(".")
        value = data
        for k in keys:
            value = value[k]
        return value

    def _set_value_from_flattened_key(self, data: dict, key: str, value: Any):
        keys = key.split(".")
        sub_dict = data
        for key in keys[:-1]:
            sub_dict = sub_dict.setdefault(key, "")
        sub_dict[keys[-1]] = value

    def _replace_globales(self, run_config_dict: dict):
        globals = run_config_dict.pop("globals")
        for global_entry, global_value in globals.items():
            for mapped_value in self.global_keys[global_entry]:
                value_from_globals = globals[global_entry]
                self._set_value_from_flattened_key(
                    data=run_config_dict, key=mapped_value, value=value_from_globals
                )

    def _replace_environment_variables(self, run_config_dict: dict):
        for config_entry, config_value in run_config_dict.items():
            if isinstance(config_value, str):
                match = re.match(self.environment_variable_pattern, config_value)
                if match:
                    environment_variable = match.group(1)
                    run_config_dict[config_entry] = os.getenv(environment_variable)


config_mapper = ConfigMapper(
    global_keys={"data_description": ["ops.train.data_description"]}
)


@graph
def cls_binary_example_graph_train():
    """Graph for training an experiment"""
    filelock_dict = acquire_locks()
    exp_context = experiment()
    exp_context, filelock_dict = train(exp_context, filelock_dict)
    exp_context, datasets, filelock_dict = prediction(exp_context, filelock_dict)
    exp_context, filelock_dict = analysis(exp_context, datasets, filelock_dict)
    release_locks(filelock_dict)
    exptests(exp_context)


cls_binary_train_example_job = JobDefinition(
    graph_def=cls_binary_example_graph_train,
    config=ConfigMapping(
        config_schema=config_mapper.build_config_schema(run_config=cls_run_config),
        config_fn=config_mapper.map_schema_to_config,
    ),
    resource_defs={"mlflow": mlflow_tracking},
)

defs = Definitions(jobs=[cls_binary_train_example_job])


if __name__ == "__main__":
    cls_binary_train_example_job.execute_in_process(
        run_config=ConfigMapping(
            config_schema=config_mapper.build_config_schema(run_config=cls_run_config),
            config_fn=config_mapper.map_schema_to_config,
        )
    )
