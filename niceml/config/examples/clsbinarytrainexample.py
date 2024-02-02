import os
from os.path import join

from dagster import JobDefinition
from dagster import RunConfig, Definitions
from dagster import graph
from keras.optimizers import Adam

from niceml.cli.clicommands import train
from niceml.config.config import InitConfig, MapInitConfig
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

data_description = ClsDataDescription(
    classes=["0", "1", "2", "3"],
    target_size=ImageSize(width=1024, height=1024),
)

ConfDirClsDataInfoListing = InitConfig.create_conf_from_class(DirClsDataInfoListing)
ConfClsDataLoader = InitConfig.create_conf_from_class(ClsDataLoader)
ConfImageInputTransformer = InitConfig.create_conf_from_class(ImageInputTransformer)
ConfTargetTransformerClassification = InitConfig.create_conf_from_class(
    TargetTransformerClassification
)

dataset_loader_train = InitConfig.create(
    KerasGenericDataset,
    batch_size=16,
    set_name="train",
    shuffle=True,
    datainfo_listing=ConfDirClsDataInfoListing(
        location=dict(uri=join(os.getenv("DATA_URI"), "number_data_split")),
        sub_dir="train",
    ),
    data_loader=ConfClsDataLoader(data_description=data_description),
    target_transformer=ConfTargetTransformerClassification(
        data_description=data_description
    ),
    input_transformer=ConfImageInputTransformer(data_description=data_description),
    net_data_logger=None,
)

dataset_loader_validation = dataset_loader_train.copy(
    update=dict(
        set_name="validation",
        datainfo_listing=dataset_loader_train.datainfo_listing.copy(
            update=dict(sub_dir="validation")
        ),
        shuffle=False,
    )
)

dataset_loader_test = dataset_loader_train.copy(
    update=dict(
        set_name="test",
        datainfo_listing=dataset_loader_train.datainfo_listing.copy(
            update=dict(sub_dir="test")
        ),
        shuffle=False,
    )
)

conf_keras_learner = InitConfig.create_conf_from_class(KerasLearner)
ConfClsMetric = InitConfig.create_conf_from_class(ClsMetric)
ConfAdam = InitConfig.create_conf_from_class(Adam, learning_rate=0.0001)
acquire_locks_config = LocksConfig(file_lock_dict={})
experiment_config = ExperimentConfig(
    exp_out_location=dict(uri=os.getenv("EXPERIMENT_URI")),
    exp_folder_pattern="CLS-$RUN_ID-id_$SHORT_ID",
)
train_config = TrainConfig(
    train_params=TrainParams(),
    model_factory=OwnMobileNetModel.create_config(),
    data_description=data_description,
    data_train=dataset_loader_train,
    data_validation=dataset_loader_validation,
    learner=conf_keras_learner(
        model_compiler=DefaultModelCompiler.create_config(
            loss="categorical_crossentropy",
            metrics=["accuracy"],
            optimizer=ConfAdam(),
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
        model_load_custom_objects=ModelCustomLoadObjects(),
    ),
    exp_initializer=ExpOutInitializer(
        exp_name="SampleCls", exp_prefix="CLS", git_modules=["niceml"]
    ),
)
train_config.learner.instantiate()

prediction_config = PredictionConfig(
    prediction_handler=VectorPredictionHandler.create_config(),
    datasets=dict(
        test=dataset_loader_test,
        validation=dataset_loader_validation,
        train_eval=dataset_loader_train.copy(update=dict(shuffle=False)),
    ),
    model_loader=KerasModelLoader(),
    prediction_function=KerasPredictionFunction(),
    prediction_steps=2,
)
prediction_config.datasets.instantiate()
analysis_config = AnalysisConfig(
    result_analyzer=DataframeAnalyzer.create_config(
        metrics=[
            InitConfig.create(
                ConfClsMetric,
                function="accuracy",
                source_col="class_idx",
                target_cols_prefix="pred_",
            ),
            InitConfig.create(
                ConfClsMetric,
                function="confusion_matrix",
                source_col="class_idx",
                target_cols_prefix="pred_",
            ),
        ]
    ),
)

exptests_config = ExpTestsConfig(
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
    config=cls_run_config,
)

defs = Definitions(jobs=[cls_binary_train_example_job])
