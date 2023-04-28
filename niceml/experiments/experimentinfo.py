"""Module for experimentinfo"""
from dataclasses import dataclass
from os.path import basename
from typing import Optional

from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem

from niceml.config.envconfig import (
    DESCRIPTION_KEY,
    ENVIRONMENT_KEY,
    EXP_DIR_KEY,
    EXP_NAME_KEY,
    EXP_PREFIX_KEY,
    EXP_TYPE_KEY,
    RUN_ID_KEY,
    SHORT_ID_KEY,
)
from niceml.utilities.idutils import ALPHANUMERICLIST
from niceml.utilities.ioutils import read_yaml


# pylint: disable = too-many-instance-attributes
@dataclass
class ExperimentInfo:
    """Dataclass which holds information about an experiment but not the data"""

    experiment_name: str
    experiment_prefix: str
    experiment_type: str
    run_id: str
    short_id: str
    environment: dict
    description: str
    exp_dir: str
    exp_filepath: Optional[str] = None

    def as_save_dict(self) -> dict:
        """Returns a dictionary which can be saved to a yaml file"""
        return {
            EXP_NAME_KEY: self.experiment_name,
            EXP_PREFIX_KEY: self.experiment_prefix,
            EXP_TYPE_KEY: self.experiment_type,
            RUN_ID_KEY: self.run_id,
            SHORT_ID_KEY: self.short_id,
            ENVIRONMENT_KEY: self.environment,
            DESCRIPTION_KEY: self.description,
            EXP_DIR_KEY: self.exp_dir,
        }


def load_exp_info(
    exp_info_file, file_system: Optional[AbstractFileSystem] = None
) -> ExperimentInfo:
    """Loads an experiment info from a yaml file"""
    file_system = file_system or LocalFileSystem()
    data = read_yaml(exp_info_file, file_system)

    exp_info = experiment_info_factory(data)
    return exp_info


def experiment_info_factory(data: dict, path: Optional[str] = None) -> ExperimentInfo:
    """Creates an experiment info from a dictionary"""
    return ExperimentInfo(
        experiment_name=data[EXP_NAME_KEY],
        experiment_prefix=data[EXP_PREFIX_KEY],
        experiment_type=data.get(EXP_TYPE_KEY, ""),
        run_id=data[RUN_ID_KEY],
        short_id=data[SHORT_ID_KEY],
        environment=data.get(ENVIRONMENT_KEY, ""),
        description=data.get(DESCRIPTION_KEY, ""),
        exp_dir=data.get(EXP_DIR_KEY, ""),
        exp_filepath=path,
    )


class ExpIdNotFoundError(Exception):
    """Exception which is raised when an experiment id is not found"""


def get_exp_id_from_name(input_name: str) -> str:
    """
    Returns a 4 digit alphanumeric string with the experiment id.
    The id follows after 'id_' and follow with a non alphanumeric char.
    """
    input_name = basename(input_name)
    index = input_name.rfind("id_")
    if index == -1:
        raise ExpIdNotFoundError(
            f"ID not found anywhere starting with 'id_': {input_name}"
        )
    cur_id = input_name[index + 3 : index + 7]
    if len(cur_id) != 4:
        raise ExpIdNotFoundError(f"ID not complete: {input_name}")
    if any((x not in ALPHANUMERICLIST for x in cur_id)):
        raise ExpIdNotFoundError(
            f"ID shouldn't have any non alphanumeric chars: {cur_id}"
        )
    return cur_id
