import os

from dagster import Config, RunConfig

from niceml.config.hydra import InitConfig
from niceml.config.ops.analysis.confopanalysis import ConfOpAnalysisClsSoftmax
from niceml.config.ops.exptests.confexptestsdefault import ConfExpTestsDefault
from niceml.config.ops.train.confoptraincls import ConfOpTrainCls
from niceml.dagster.ops.analysis import AnalysisConfig
from niceml.dagster.ops.experiment import ExperimentConfig
from niceml.dagster.ops.filelockops import LocksConfig
from niceml.dagster.ops.prediction import PredictionConfig
from niceml.dagster.ops.train import TrainConfig
from niceml.mlcomponents.resultanalyzers.dataframes.dfanalyzer import DataframeAnalyzer
from niceml.utilities.omegaconfutils import register_niceml_resolvers


class ConfResultAnalyzer(InitConfig):
    target: str = InitConfig.create_target_field(DataframeAnalyzer)


class ConfOpAnalysis(AnalysisConfig):
    result_analyzer_ = dict()


class CLSOpConfig(Config):
    acquire_locks: LocksConfig
    experiment: ExperimentConfig
    train: TrainConfig
    prediction: PredictionConfig
    analysis: AnalysisConfig
    exptests: ConfExpTestsDefault


register_niceml_resolvers()
cls_run_config = RunConfig(
    ops={
        "acquire_locks": LocksConfig(file_lock_dict={}),
        "experiment": ExperimentConfig(),
        "train": ConfOpTrainCls(),
        "prediction": PredictionConfig(),
        "analysis": ConfOpAnalysisClsSoftmax(),
        "exptests": ConfExpTestsDefault(),
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


def config_fn(input_config):
    return input_config


# train_config_mapping = ConfigMapping(config_fn=config_fn, config_schema=CLSJobConfig)
