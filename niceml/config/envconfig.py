"""Module for extracting information from the environment"""
from os import getenv
from typing import Optional

RUN_ID_KEY = "RUN_ID"
SHORT_ID_KEY = "SHORT_ID"
PIPELINE_KEY = "PIPELINE"
EXP_NAME_KEY = "EXPERIMENT_NAME"
EXP_PREFIX_KEY = "EXPERIMENT_PREFIX"
EXP_TYPE_KEY = "EXPERIMENT_TYPE"
EXP_DIR_KEY = "EXPERIMENT_DIR"
ENVIRONMENT_KEY = "ENVIRONMENT"
DESCRIPTION_KEY = "DESCRIPTION"
LOCAL_EXP_CACHE_PATH_KEY = "LOCAL_EXP_CACHE_PATH"


def replace_id_keys(input_str: str, short_id: str, run_id: str) -> str:
    """Replaces the keys $SHORT_ID and $RUN_ID with their actual values"""
    input_str = input_str.replace("$" + SHORT_ID_KEY, short_id)
    input_str = input_str.replace("$" + RUN_ID_KEY, run_id)

    return input_str


def get_local_exp_cache_path() -> Optional[str]:
    """Returns path of local exp cache from environment"""
    return getenv(LOCAL_EXP_CACHE_PATH_KEY, None)
