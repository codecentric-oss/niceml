"""Module for fsspec storage"""
import logging
from enum import Enum
from os import makedirs
from os.path import dirname, isdir, relpath
from typing import List, Optional

from fsspec import AbstractFileSystem

from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.expfilenames import filter_for_exp_info_files
from niceml.experiments.loadexpinfo import load_exp_info
from niceml.utilities.ioutils import list_dir

_logger = logging.getLogger(__name__)


class FsFileSystemStorage(StorageInterface):
    """A CloudStorageInterface to interact with fsspec isntances"""

    def __init__(self, file_system: AbstractFileSystem, root_dir: str):
        """
        Creates a new FSSpecStorage instance.
        """
        self.file_system = file_system
        self.root_dir = root_dir

    def list_data(self, path: Optional[str] = None) -> List[str]:
        """recusively lists all objects in the given path"""
        target_path = (
            self.root_dir if path is None else self.join_paths(self.root_dir, path)
        )
        item_list = list_dir(
            target_path,
            return_full_path=True,
            recursive=True,
            file_system=self.file_system,
        )
        item_list = [relpath(cur_file, self.root_dir) for cur_file in item_list]
        return item_list

    def download_data(self, bucket_path: str, local_path: str, recursive: bool = True):
        """downloads a given object to the specified local_path

        Raises:
            RuntimeError:
                If the given bucket_path is not part of the currently opended
                filesystem.
        """
        local_dir = dirname(local_path)
        if not isdir(local_dir):
            makedirs(local_dir)
        self.file_system.download(
            self.join_paths(self.root_dir, bucket_path), local_path, recursive=recursive
        )

    def download_as_str(self, bucket_path: str) -> str:
        """returns the given bucket_path content as string

        Raises:
            RuntimeError:
                If the given bucket_path is not part of the currently opended
                filesystem.
        """

        return self.file_system.cat(self.join_paths(self.root_dir, bucket_path))

    def join_paths(self, *paths: str) -> str:
        """joins the given paths with the fsspec specific path seperator"""
        paths = [path for path in paths if len(path) > 0]
        return self.file_system.sep.join(paths)

    def list_experiments(self, path: Optional[str] = None) -> List[ExperimentInfo]:
        files = self.list_data(path)
        files = filter_for_exp_info_files(files)
        exp_info_list = []
        for cur_file in files:
            try:
                exp_info_list.append(load_exp_info(self, dirname(cur_file)))
            except FileNotFoundError:
                _logger.warning("Experiment couldn't be loaded: %s", cur_file)
        return exp_info_list
