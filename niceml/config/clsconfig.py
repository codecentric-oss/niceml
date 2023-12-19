import os

from dagster import Config, RunConfig
from dagster_mlflow import mlflow_tracking

from niceml.dagster.ops.analysis import AnalysisConfig
from niceml.dagster.ops.experiment import ExperimentConfig
from niceml.dagster.ops.exptests import ExpTestsConfig
from niceml.dagster.ops.filelockops import LocksConfig
from niceml.dagster.ops.prediction import PredictionConfig
from niceml.dagster.ops.train import TrainConfig
from niceml.scripts.hydraconfreader import load_hydra_conf
from niceml.utilities.ioutils import read_yaml
from niceml.utilities.omegaconfutils import register_niceml_resolvers


class CLSOpConfig(Config):
    acquire_locks: LocksConfig
    experiment: ExperimentConfig
    train: TrainConfig
    prediction: PredictionConfig
    analysis: AnalysisConfig
    exptests: ExpTestsConfig


# class CLSJobConfig(Config):
#     ops: str = Field(
#         description="bla"
#     )
register_niceml_resolvers()
cls_run_config = RunConfig(
    ops={
        "acquire_locks": LocksConfig(file_lock_dict={}),
        "experiment": ExperimentConfig(),
        "train": TrainConfig(
            # **load_hydra_conf(
            #     conf_path="configs/ops/train/op_train_cls_binary_save.yaml"
            # )
        ),
        "prediction": PredictionConfig(),
        "analysis": AnalysisConfig(
            **read_yaml(filepath="configs/ops/analysis/op_analysis_cls_softmax.yaml")
        ),
        "exptests": ExpTestsConfig(
            tests=read_yaml(filepath="configs/ops/exptests/exptests_default.yaml")[
                "test_list"
            ]
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


def config_fn(input_config):
    return input_config


# train_config_mapping = ConfigMapping(config_fn=config_fn, config_schema=CLSJobConfig)
