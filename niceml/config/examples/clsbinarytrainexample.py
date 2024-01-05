import os
from os.path import join

from dagster import JobDefinition
from dagster import RunConfig, Definitions
from keras.optimizers import Adam

from niceml.config.config import InitConfig
from niceml.config.trainparams import TrainParams
from niceml.dagster.jobs.graphs import (
    graph_train,
)
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

ConfKearLearner = InitConfig.create_conf_from_class(KerasLearner)
ConfAdam = InitConfig.create_conf_from_class(Adam)
ConfClsMetric = InitConfig.create_conf_from_class(ClsMetric)

acquire_locks = LocksConfig(file_lock_dict={})
experiment = ExperimentConfig(
    exp_out_location=dict(uri=os.getenv("EXPERIMENT_URI")),
    exp_folder_pattern="CLS-$RUN_ID-id_$SHORT_ID",
)
train = TrainConfig(
    train_params=TrainParams(),
    model_factory=OwnMobileNetModel.create_model(),
    data_description=data_description,
    data_train=dataset_loader_train,
    dataset_validation=dataset_loader_validation,
    learner=ConfKearLearner(
        model_compiler=DefaultModelCompiler.create_config(
            loss="categorical_crossentropy",
            metrics=["accuracy"],
            optimizer=ConfAdam(learning_rate=0.0001),
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
)

prediction = PredictionConfig(
    prediction_handler=VectorPredictionHandler(),
    datasets=dict(
        test=dataset_loader_test,
        validation=dataset_loader_validation,
        train_eval=dataset_loader_train.copy(update=dict(shuffle=False)),
    ),
    model_loader=KerasModelLoader(),
    prediction_function=KerasPredictionFunction(),
    prediction_steps=2,
)

analysis = AnalysisConfig(
    result_analyzer=DataframeAnalyzer(
        metrics=[
            ConfClsMetric(
                function="accuracy",
                source_col="class_idx",
                target_cols_prefix="pred_",
            ),
            ConfClsMetric(
                function="confusion_matrix",
                source_col="class_idx",
                target_cols_prefix="pred_",
            ),
        ]
    ),
)

exptests = ExpTestsConfig(
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
        "acquire_locks": acquire_locks,
        "experiment": experiment,
        "train": train,
        "prediction": prediction,
        "analysis": analysis,
        "exptests": exptests,
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

cls_binary_train_example_job = JobDefinition(
    graph_def=graph_train, config=cls_run_config
)
defs = Definitions(jobs=[cls_binary_train_example_job])
