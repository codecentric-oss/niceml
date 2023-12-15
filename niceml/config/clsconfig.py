from dagster import Config, RunConfig
from dagster_mlflow import mlflow_tracking

from niceml.dagster.ops.analysis import AnalysisConfig
from niceml.dagster.ops.experiment import ExperimentConfig
from niceml.dagster.ops.exptests import ExpTestsConfig
from niceml.dagster.ops.filelockops import LocksConfig
from niceml.dagster.ops.prediction import PredictionConfig
from niceml.dagster.ops.train import TrainConfig


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

cls_run_config = RunConfig(
    ops={
        "acquire_locks": LocksConfig(),
        "experiment": ExperimentConfig(),
        "train": TrainConfig(),
        "prediction": PredictionConfig(),
        "analysis": AnalysisConfig(),
        "exptests": ExpTestsConfig(),
    },
    resources={"mlflow": mlflow_tracking()},  # TODO: here is an error
)


def config_fn(input_config):
    return input_config


# train_config_mapping = ConfigMapping(config_fn=config_fn, config_schema=CLSJobConfig)
