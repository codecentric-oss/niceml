"""Module for the analysis dagster op"""
from typing import Dict, Tuple, List

from dagster import OpExecutionContext, op, Out, Config
from hydra.utils import ConvertMode, instantiate
from pydantic import Field

from niceml.config.defaultremoveconfigkeys import DEFAULT_REMOVE_CONFIG_KEYS
from niceml.config.hydra import create_hydra_init_field
from niceml.config.writeopconfig import write_op_config
from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import OpNames
from niceml.mlcomponents.resultanalyzers.analyzer import ResultAnalyzer
from niceml.utilities.readwritelock import FileLock


class AnalysisConfig(Config):
    result_analyzer_: dict = create_hydra_init_field(
        target_class=ResultAnalyzer, alias="result_analyzer"
    )
    remove_key_list: List[str] = Field(
        default=DEFAULT_REMOVE_CONFIG_KEYS,
        description="These key are removed from any config recursively before it is saved.",
    )  # TODO: refactor

    @property
    def result_analyzer(self) -> ResultAnalyzer:
        return instantiate(self.result_analyzer_, _convert_=ConvertMode.ALL)


# pylint: disable=use-dict-literal
@op(
    out={"expcontext": Out(), "filelock_dict": Out()},
    required_resource_keys={"mlflow"},
)
def analysis(
    context: OpExecutionContext,
    exp_context: ExperimentContext,
    datasets: Dict[str, Dataset],
    filelock_dict: Dict[str, FileLock],
    config: AnalysisConfig,
) -> Tuple[ExperimentContext, Dict[str, FileLock]]:
    """This dagster op reads the predictions and calculates metrics defined in config
    (result_analyser)"""
    write_op_config(
        config, exp_context, OpNames.OP_ANALYSIS.value, config.remove_key_list
    )
    data_description: DataDescription = (
        exp_context.instantiate_datadescription_from_yaml()
    )

    config.result_analyzer.initialize(data_description)

    for dataset_key, cur_pred_set in datasets.items():
        context.log.info(f"Analyze dataset: {dataset_key}")
        cur_pred_set.initialize(data_description, exp_context)
        config.result_analyzer(cur_pred_set, exp_context, dataset_key)

    return exp_context, filelock_dict
