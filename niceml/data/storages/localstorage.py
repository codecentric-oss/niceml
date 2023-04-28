"""Module for local storage"""
import shutil
from os.path import dirname, join, relpath
from typing import List, Optional

from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.expfilenames import filter_for_exp_info_files
from niceml.experiments.loadexpinfo import load_exp_info
from niceml.utilities.ioutils import list_dir


class LocalStorage(StorageInterface):
    """Implementation of StorageInterface for local storage"""

    def __init__(self, working_directory: Optional[str] = None):
        self.working_directory = working_directory

    def list_data(self, path: Optional[str] = None) -> List[str]:
        target_dir = self._get_target_path(path)

        files = list_dir(target_dir, recursive=True, return_full_path=True)
        if self.working_directory is not None:
            files = [relpath(cur_file, self.working_directory) for cur_file in files]
        return files

    def _get_target_path(self, path: Optional[str]) -> str:
        """Returns the path to the file or directory, checking if
        the working directory and the path is"""
        if path is None and self.working_directory is None:
            raise ValueError("path must be provided if working_directory is not set")
        if path is None:
            target_path = self.working_directory
        elif self.working_directory is None:
            target_path = path
        else:
            target_path = join(self.working_directory, path)
        return target_path

    def download_data(self, bucket_path: str, local_path: str):
        target_path = self._get_target_path(bucket_path)
        shutil.copyfile(target_path, local_path)

    def download_as_str(self, bucket_path: str) -> bytes:
        target_path = self._get_target_path(bucket_path)
        with open(target_path, "rb") as file:
            data = file.read()
        return data

    def list_experiments(self, path: Optional[str] = None) -> List[ExperimentInfo]:
        files = self.list_data(path)
        files = filter_for_exp_info_files(files)
        exp_info_list = [load_exp_info(self, dirname(cur_path)) for cur_path in files]
        return exp_info_list

    def join_paths(self, *paths) -> str:
        return join(*paths)
