""" List of experiment filenames """
from enum import Enum
from os.path import basename, join
from typing import List, Optional

from niceml.config.subsetnames import get_eval_save_names


class ExperimentFilenames:  # pylint: disable=too-few-public-methods
    """Available experiment filenames"""

    CONFIGS_FOLDER: str = "configs"
    MODELS_FOLDER: str = "models"
    EXP_INFO: str = "experiment_info.yaml"
    DATA_DESCRIPTION: str = "data_description.yaml"
    EXP_TESTS: str = "exp_tests.csv"
    TRAIN_LOGS: str = "train_logs.csv"
    STATS_TRAIN: str = "stats_train.yaml"
    STATS_PRED: str = "stats_prediction.yaml"
    GIT_VERSIONS: str = "git_versions.yaml"
    CUSTOM_LOAD_OBJECTS: str = "model_load_custom_objects.yaml"
    ANALYSIS_FILE: str = "result_{dataset_name}.yaml"
    ANALYSIS_FOLDER: str = "analysis"
    EPOCHS_FORMATTING: str = "ep{epoch:03d}"
    DATASETS_STATS_FOLDER: str = "datasetsstats"
    PREDICTION_FOLDER: str = "predictions"
    EXTERNAL_INFOS: str = "external_infos"
    NET_DATA_FOLDER: str = "net_data"
    EXP_FILES_FILE: str = "exp_files.parq"
    EXP_FILES_COL: str = "exp_files"


class OpNames(str, Enum):
    """Names of the ops"""

    OP_TRAIN = "train"
    OP_EXPTESTS = "exptests"
    OP_ANALYSIS = "analysis"
    OP_PREDICTION = "prediction"
    OP_EXPERIMENT = "experiment"


def filter_for_exp_info_files(file_list: List[str]) -> List[str]:
    """Returns all files which are named like the EXP_INFO file"""
    return [x for x in file_list if basename(x) in [ExperimentFilenames.EXP_INFO]]


class AdditionalExperimentFilenames(str, Enum):
    """Experiment filenames used dataset specific"""

    CLS_RESULTS = join(ExperimentFilenames.PREDICTION_FOLDER, "{dataset}.parq")

    def get_complete_name(self, dataset_name: str) -> str:
        """Replaces {dataset} with the specific datasetname and returns the string"""
        return self.value.format(dataset=dataset_name)

    def get_formatted_basename(self, dataset_name: str) -> str:
        """returns only the basename from the complete_name"""
        return basename(self.get_complete_name(dataset_name))


def get_load_parq_files() -> List[str]:
    """returns the files which should be loaded"""
    cur_exp_fn: AdditionalExperimentFilenames
    load_parq_files = [
        cur_exp_fn.get_complete_name(y)
        for cur_exp_fn in AdditionalExperimentFilenames
        for y in get_eval_save_names()
    ]
    return load_parq_files


class ExpEvalCopyNames:  # pylint: disable=too-few-public-methods
    """Class for determining whether a file should be copied during eval job"""

    def __init__(self, exclude_files: Optional[List[str]] = None):
        self.exclude_files = exclude_files or [
            ExperimentFilenames.ANALYSIS_FOLDER,
            ExperimentFilenames.PREDICTION_FOLDER,
        ]

    def __contains__(self, key: str) -> bool:
        for ex_file in self.exclude_files:
            if key.startswith(ex_file):
                return False
        return True
