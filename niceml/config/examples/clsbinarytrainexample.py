import os
from os.path import join
from typing import List, Dict

from dagster import JobDefinition, ConfigSchema, ConfigMapping
from dagster import RunConfig, Definitions
from dagster import graph
from dagster_mlflow import mlflow_tracking
from keras.optimizers import Adam

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
        config_schema=build_config_schema(
            run_config=cls_run_config, global_keys=["data_description"]
        ),
        config_fn=build_config,
    ),
    resource_defs={"mlflow": mlflow_tracking},
)

defs = Definitions(jobs=[cls_binary_train_example_job])


if __name__ == "__main__":
    cls_binary_train_example_job.execute_in_process()
