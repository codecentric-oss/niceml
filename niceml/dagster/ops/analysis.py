"""Module for the analysis dagster op"""
import json
from os.path import join
from typing import Dict, Tuple

from hydra.utils import ConvertMode, instantiate

from niceml.config.hydra import HydraInitField, instantiate_from_yaml
from niceml.config.writeopconfig import write_op_config
from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import ExperimentFilenames, OpNames
from niceml.mlcomponents.resultanalyzers.analyzer import ResultAnalyzer
from niceml.utilities.fsspec.locationutils import open_location
from dagster import OpExecutionContext, op, Out

from niceml.utilities.readwritelock import FileLock


# pylint: disable=use-dict-literal
@op(
    config_schema=dict(result_analyzer=HydraInitField(ResultAnalyzer)),
    out={"expcontext": Out(), "filelock_dict": Out()},
)
def analysis(
    context: OpExecutionContext,
    exp_context: ExperimentContext,
    filelock_dict: Dict[str, FileLock],
) -> Tuple[ExperimentContext, Dict[str, FileLock]]:
    """This dagster op analysis the previous predictions applied by the model"""
    op_config = json.loads(json.dumps(context.op_config))
    write_op_config(op_config, exp_context, OpNames.OP_ANALYSIS.value)
    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)
    data_description: DataDescription = (
        exp_context.instantiate_datadescription_from_yaml()
    )

    result_analyzer: ResultAnalyzer = instantiated_op_config["result_analyzer"]
    result_analyzer.initialize(data_description)
    with open_location(exp_context.fs_config) as (exp_fs, exp_root):
        datasets_dict: Dict[str, Dataset] = instantiate_from_yaml(
            join(
                exp_root,
                ExperimentFilenames.CONFIGS_FOLDER,
                OpNames.OP_PREDICTION,
                "datasets.yaml",
            ),
            file_system=exp_fs,
        )
    for dataset_key, cur_pred_set in datasets_dict.items():
        context.log.info(f"Analyze dataset: {dataset_key}")
        cur_pred_set.initialize(data_description, exp_context)
        result_analyzer(cur_pred_set, exp_context, dataset_key)

    return exp_context, filelock_dict
