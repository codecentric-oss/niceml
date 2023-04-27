"""Module for the subset names"""
from typing import List


class SubsetNames:  # pylint: disable=too-few-public-methods
    """names for datasets in datasets.yml"""

    TRAIN: str = "train"
    TEST: str = "test"
    VALIDATION: str = "validation"
    TRAIN_EVAL: str = "train_eval"


def get_save_name(dataset_name: str) -> str:
    """Removes only the data_ prefix"""
    if dataset_name.startswith("data_"):
        return dataset_name[5:]
    return dataset_name


EVAL_DATASET_LIST: List[str] = [
    SubsetNames.TEST,
    SubsetNames.VALIDATION,
    SubsetNames.TRAIN_EVAL,
]


def get_eval_save_names() -> List[str]:
    """Returns the names for the evaluation dataset names"""
    return [get_save_name(x) for x in EVAL_DATASET_LIST]
