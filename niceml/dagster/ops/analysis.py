"""Module for the analysis dagster op"""
import json
from typing import Dict, Tuple

from hydra.utils import ConvertMode, instantiate

from niceml.config.defaultremoveconfigkeys import DEFAULT_REMOVE_CONFIG_KEYS
from niceml.config.hydra import HydraInitField
from niceml.config.writeopconfig import write_op_config
from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import OpNames
from niceml.mlcomponents.resultanalyzers.analyzer import ResultAnalyzer
from dagster import OpExecutionContext, op, Out, Field

from niceml.utilities.readwritelock import FileLock


# pylint: disable=use-dict-literal
@op(
    config_schema=dict(
        result_analyzer=HydraInitField(ResultAnalyzer),
        remove_key_list=Field(
            list,
            default_value=DEFAULT_REMOVE_CONFIG_KEYS,
            description="These key are removed from any config recursively before it is saved.",
        ),
    ),
    out={"expcontext": Out(), "filelock_dict": Out()},
    required_resource_keys={"mlflow"},
)
def analysis(
    context: OpExecutionContext,
    exp_context: ExperimentContext,
    datasets: Dict[str, Dataset],
    filelock_dict: Dict[str, FileLock],
) -> Tuple[ExperimentContext, Dict[str, FileLock]]:
    """This dagster op analysis the previous predictions applied by the model"""
    op_config = json.loads(json.dumps(context.op_config))
    write_op_config(
        op_config, exp_context, OpNames.OP_ANALYSIS.value, op_config["remove_key_list"]
    )
    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)
    data_description: DataDescription = (
        exp_context.instantiate_datadescription_from_yaml()
    )

    result_analyzer: ResultAnalyzer = instantiated_op_config["result_analyzer"]
    result_analyzer.initialize(
        data_description=data_description, exp_context=exp_context
    )

    for dataset_key, cur_pred_set in datasets.items():
        context.log.info(f"Analyze dataset: {dataset_key}")
        cur_pred_set.initialize(data_description, exp_context)
        result_analyzer(cur_pred_set, exp_context, dataset_key)

    return exp_context, filelock_dict
