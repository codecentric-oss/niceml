import os
from os.path import join

from dagster import RunConfig
from keras.optimizers import Adam
from keyring.core import load_env

from niceml.config.defaultremoveconfigkeys import DEFAULT_REMOVE_CONFIG_KEYS
from niceml.config.trainparams import TrainParams
from niceml.dagster.ops.analysis import AnalysisConfig
from niceml.dagster.ops.experiment import ExperimentConfig
from niceml.dagster.ops.exptests import ExpTestsConfig
from niceml.dagster.ops.filelockops import LocksConfig
from niceml.dagster.ops.prediction import PredictionConfig
from niceml.dagster.ops.train import TrainConfig
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

load_env()

dataset_train = KerasGenericDataset(
    batch_size=16,
    set_name="train",
    shuffle=True,
    datainfo_listing=DirClsDataInfoListing(
        location=dict(uri=join(os.getenv("DATA_URI"), "number_data_split")),
        sub_dir="train",
    ),
    data_loader=ClsDataLoader(
        data_description=ClsDataDescription(
            classes=["0", "1", "2", "3"],
            target_size=ImageSize(width=1024, height=1024),
        ),
    ),
    target_transformer=TargetTransformerClassification(),
    input_transformer=ImageInputTransformer(),
)

dataset_validation = dataset_train
dataset_validation.set_name = "validation"
dataset_validation.datainfo_listing.sub_dir = "validation"
dataset_validation.shuffle = False
dataset_test = dataset_train
dataset_test.set_name = "test"
dataset_test.shuffle = False
dataset_test.datainfo_listing.sub_dir = "test"

cls_run_config = RunConfig(
    ops={
        "acquire_locks": LocksConfig.create(file_lock_dict={}),
        "experiment": ExperimentConfig.create(
            exp_out_location=dict(uri=os.getenv("EXPERIMENT_URI")),
            exp_folder_pattern="CLS-$RUN_ID-id_$SHORT_ID",
        ),
        "train": TrainConfig.create(
            train_params=TrainParams(steps_per_epoch=2, validation_steps=2),
            model_factory=OwnMobileNetModel(),
            data_description=ClsDataDescription(
                classes=["0", "1", "2", "3"],
                target_size=ImageSize(width=1024, height=1024),
            ),
            data_train=KerasGenericDataset(
                batch_size=16,
                set_name="train",
                shuffle=True,
                datainfo_listing=DirClsDataInfoListing(
                    location=dict(uri=join(os.getenv("DATA_URI"), "number_data_split")),
                    sub_dir="train",
                ),
                data_loader=ClsDataLoader(
                    data_description=ClsDataDescription(
                        classes=["0", "1", "2", "3"],
                        target_size=ImageSize(width=1024, height=1024),
                    ),
                ),
                target_transformer=TargetTransformerClassification(),
                input_transformer=ImageInputTransformer(),
            ),
            dataset_validation=KerasGenericDataset(
                batch_size=16,
                set_name="validation",
                shuffle=True,
                datainfo_listing=DirClsDataInfoListing(
                    location=dict(uri=join(os.getenv("DATA_URI"), "number_data_split")),
                    sub_dir="validation",
                ),
                data_loader=ClsDataLoader(
                    data_description=ClsDataDescription(
                        classes=["0", "1", "2", "3"],
                        target_size=ImageSize(width=1024, height=1024),
                    ),
                ),
                target_transformer=TargetTransformerClassification(),
                input_transformer=ImageInputTransformer(),
            ),
            learner=KerasLearner(
                model_compiler=DefaultModelCompiler(
                    loss="categorical_crossentropy",
                    metrics=["accuracy"],
                    optimizer=Adam(learning_rate=0.0001),
                ),
                callback_initializer=CallbackInitializer(
                    callback_list=[
                        InitCallbackFactory(callback=LossNanCheckCallback()),
                        LoggingOutputCallbackFactory(),
                    ],
                    callback_dict=dict(
                        save_model=ModelCallbackFactory(
                            model_subfolder="models/model-id_{short_id}-ep{epoch:03d}.hdf5"
                        )
                    ),
                ),
                model_load_custom_objects=ModelCustomLoadObjects(),
            ),
            exp_initializer=ExpOutInitializer(
                exp_name="SampleCls", exp_prefix="CLS", git_modules=["niceml"]
            ),
            remove_key_list=DEFAULT_REMOVE_CONFIG_KEYS,
        ),
        "prediction": PredictionConfig.create(
            prediction_handler=VectorPredictionHandler(),
            datasets=dict(
                test=KerasGenericDataset(
                    batch_size=16,
                    set_name="test",
                    shuffle=True,
                    datainfo_listing=DirClsDataInfoListing(
                        location=dict(
                            uri=join(os.getenv("DATA_URI"), "number_data_split")
                        ),
                        sub_dir="test",
                    ),
                    data_loader=ClsDataLoader(
                        data_description=ClsDataDescription(
                            classes=["0", "1", "2", "3"],
                            target_size=ImageSize(width=1024, height=1024),
                        ),
                    ),
                    target_transformer=TargetTransformerClassification(),
                    input_transformer=ImageInputTransformer(),
                ),
                validation=KerasGenericDataset(
                    batch_size=16,
                    set_name="validation",
                    shuffle=True,
                    datainfo_listing=DirClsDataInfoListing(
                        location=dict(
                            uri=join(os.getenv("DATA_URI"), "number_data_split")
                        ),
                        sub_dir="validation",
                    ),
                    data_loader=ClsDataLoader(
                        data_description=ClsDataDescription(
                            classes=["0", "1", "2", "3"],
                            target_size=ImageSize(width=1024, height=1024),
                        ),
                    ),
                    target_transformer=TargetTransformerClassification(),
                    input_transformer=ImageInputTransformer(),
                ),
                train_eval=KerasGenericDataset(
                    batch_size=16,
                    set_name="train",
                    shuffle=True,
                    datainfo_listing=DirClsDataInfoListing(
                        location=dict(
                            uri=join(os.getenv("DATA_URI"), "number_data_split")
                        ),
                        sub_dir="train",
                    ),
                    data_loader=ClsDataLoader(
                        data_description=ClsDataDescription(
                            classes=["0", "1", "2", "3"],
                            target_size=ImageSize(width=1024, height=1024),
                        ),
                    ),
                    target_transformer=TargetTransformerClassification(
                        data_description=ClsDataDescription(
                            classes=["0", "1", "2", "3"],
                            target_size=ImageSize(width=1024, height=1024),
                        ),
                    ),
                    input_transformer=ImageInputTransformer(
                        data_description=ClsDataDescription(
                            classes=["0", "1", "2", "3"],
                            target_size=ImageSize(width=1024, height=1024),
                        ),
                    ),
                ),
            ),
            model_loader=KerasModelLoader(),
            prediction_function=KerasPredictionFunction(),
            prediction_steps=2,
        ),
        "analysis": AnalysisConfig.create(
            result_analyzer=DataframeAnalyzer(
                metrics=[
                    ClsMetric(
                        function="accuracy",
                        source_col="class_idx",
                        target_cols_prefix="pred_",
                    ),
                    ClsMetric(
                        function="confusion_matrix",
                        source_col="class_idx",
                        target_cols_prefix="pred_",
                    ),
                ]
            )
        ),
        "exptests": ExpTestsConfig.create(
            exp_test_process=ExpTestProcess(
                test_list=[
                    ModelsSavedExpTest(),
                    ParqFilesNoNoneExpTest(),
                    ExpEmptyTest(),
                    CheckFilesFoldersTest(
                        folders=["configs"],
                        files=[
                            "configs/train/data_description.yaml",
                            "train_logs.csv",
                            "experiment_info.yaml",
                        ],
                    ),
                ]
            )
        ),
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
