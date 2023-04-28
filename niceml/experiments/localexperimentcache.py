"""Implementation of the ExperimentCache interface for local experiments."""
from abc import ABC, abstractmethod
from os import makedirs
from os.path import dirname, isdir, join, split, splitext
from typing import List, Optional

import pandas as pd
import yaml

from niceml.data.dataloaders.interfaces.dfloader import DfLoader
from niceml.data.dataloaders.interfaces.imageloader import ImageLoader
from niceml.data.storages.localstorage import LocalStorage
from niceml.experiments.expdatastorageloader import create_expdata_from_storage
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentinfo import ExpIdNotFoundError
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.utilities.ioutils import list_dir, write_parquet
from niceml.utilities.regexutils import check_exp_name


class ExperimentCache(ABC):
    """Interface for the experiment cache"""

    @abstractmethod
    def __contains__(self, exp_id: str) -> bool:
        """Checks if the experiment is in the cache"""

    @abstractmethod
    def get_exp_count_in_cache(self) -> int:
        """Returns the amount of cached experiments"""

    @abstractmethod
    def load_experiment(
        self,
        exp_id: str,
        image_loader: Optional[ImageLoader] = None,
        df_loader: Optional[DfLoader] = None,
    ) -> ExperimentData:
        """Loads the experiment from the cache"""

    @abstractmethod
    def save_experiment(self, exp_data: ExperimentData):
        """Saves the experiment to the cache"""


def create_exp_file_df(exp_data: ExperimentData) -> pd.DataFrame:
    """Creates a dataframe with the experiment files"""
    exp_files = []
    for exp_file in exp_data.all_exp_files:
        ext = splitext(exp_file)[1]

        if len(ext) > 0:
            if ext == ".yml":
                ext = ".yaml"
            exp_files.append(
                {
                    ExperimentFilenames.EXP_FILES_COL: splitext(exp_file)[0] + ext,
                    "suffix": ext,
                }
            )
    return pd.DataFrame(exp_files)


def get_exp_folder_list(folder: str, root_folder: Optional[str] = None) -> List[str]:
    """
        Creates a list with names of experiment folders, which also includes parent
         directories if they exist
    Args:
        folder: folder to search in
        root_folder: param for saving the first `folder` attribute due to a recursive function call

    Returns:
        List of experiment folder names

    """
    if check_exp_name(folder):
        return [folder]

    folders = (
        list_dir(folder) if root_folder is None else list_dir(join(root_folder, folder))
    )
    if root_folder is None:
        root_folder = folder
    if not all(check_exp_name(split(path)[-1]) for path in folders):
        sub_folders = [
            get_exp_folder_list(path, root_folder)
            for path in folders
            if isdir(join(root_folder, path))
        ]
        sub_folders = sum(sub_folders, [])
        return sub_folders
    return (
        [join(folder, sub_folder) for sub_folder in folders]
        if folder != root_folder
        else folders
    )


class LocalExperimentCache(ExperimentCache):
    """Implementation of the ExperimentCache interface for local disk experiments."""

    def __init__(self, store_folder: str):
        self.store_folder = store_folder
        if not isdir(self.store_folder):
            makedirs(self.store_folder, exist_ok=True)

    def __contains__(self, exp_id: str) -> bool:
        try:
            self.find_folder_name_of_exp_id(exp_id)
            return True
        except ExpIdNotFoundError:
            return False

    def get_exp_count_in_cache(self):
        return len(get_exp_folder_list(self.store_folder))

    def find_folder_name_of_exp_id(self, exp_id) -> Optional[str]:
        """Finds the folder name of the experiment id"""

        for folder_name in get_exp_folder_list(self.store_folder):
            if exp_id in folder_name and isdir(join(self.store_folder, folder_name)):
                return folder_name
        raise ExpIdNotFoundError(f"Experiment with id: {exp_id} not in Cache")

    def load_experiment(
        self,
        exp_id: str,
        image_loader: Optional[ImageLoader] = None,
        df_loader: Optional[DfLoader] = None,
    ) -> ExperimentData:
        """Loads the experiment from the cache"""
        exp_folder = self.find_folder_name_of_exp_id(exp_id)
        storage = LocalStorage(self.store_folder)
        return create_expdata_from_storage(
            exp_folder, storage, image_loader=image_loader, df_loader=df_loader
        )

    def save_experiment(self, exp_data: ExperimentData):
        if self.store_folder is None:
            return
        self._create_output_folders(exp_data=exp_data)

        exp_files_df = create_exp_file_df(exp_data=exp_data)

        for key, value in exp_data.exp_dict_data.items():
            with open(
                join(
                    self.store_folder,
                    exp_data.get_experiment_path(),
                    key + ".yaml",
                ),
                "w",
                encoding="utf-8",
            ) as exp_data_path:
                yaml.dump(value, exp_data_path, indent=2)

        exp_data.log_data.to_csv(
            join(
                self.store_folder,
                exp_data.get_experiment_path(),
                ExperimentFilenames.TRAIN_LOGS,
            )
        )

        write_parquet(
            exp_files_df,
            join(
                self.store_folder,
                exp_data.get_experiment_path(),
                ExperimentFilenames.EXP_FILES_FILE,
            ),
        )

    def _create_output_folders(self, exp_data: ExperimentData):
        """Creates the output folders for the experiment"""
        folder_list: List[str] = [
            dirname(exp_file) for exp_file in exp_data.all_exp_files
        ]
        for folder in set(folder_list):
            makedirs(
                name=join(self.store_folder, exp_data.get_experiment_path(), folder),
                exist_ok=True,
            )
