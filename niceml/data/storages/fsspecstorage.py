"""Module for fsspec storage"""
import logging
from enum import Enum
from os import makedirs
from os.path import dirname, isdir, relpath
from typing import Any, Dict, List, Optional, Union

from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.expfilenames import filter_for_exp_info_files
from niceml.experiments.loadexpinfo import load_exp_info
from niceml.utilities.fsspec.locationutils import LocationConfig, open_location
from niceml.utilities.ioutils import list_dir

_logger = logging.getLogger(__name__)


class _ItemTypes(str, Enum):
    DIRECTORY = "directory"
    FILE = "file"


class FSSpecStorage(StorageInterface):
    """A CloudStorageInterface to interact with fsspec isntances"""

    def __init__(self, fsconfig: Union[LocationConfig, Dict[str, Any]]):
        """
        Creates a new FSSpecStorage instance.

        Args:
            fsconfig (FSSpecStorage | Dict[str, Any]):
                The fsspec configuration to open the filesystem with
        """
        self._fsconfig = fsconfig

    def list_data(self, path: Optional[str] = None) -> List[str]:
        """recusively lists all objects in the given path"""
        with open_location(self._fsconfig) as (filesystem, fspath):
            target_path = fspath if path is None else self.join_paths(fspath, path)
            item_list = list_dir(
                target_path,
                return_full_path=True,
                recursive=True,
                file_system=filesystem,
            )
            item_list = [relpath(cur_file, fspath) for cur_file in item_list]
        return item_list

    def download_data(self, bucket_path: str, local_path: str, recursive: bool = True):
        """downloads a given object to the specified local_path

        Raises:
            RuntimeError:
                If the given bucket_path is not part of the currently opended
                filesystem.
        """
        with open_location(self._fsconfig) as (filesystem, path):
            local_dir = dirname(local_path)
            if not isdir(local_dir):
                makedirs(local_dir)
            filesystem.download(
                self.join_paths(path, bucket_path), local_path, recursive=recursive
            )

    def download_as_str(self, bucket_path: str) -> str:
        """returns the given bucket_path content as string

        Raises:
            RuntimeError:
                If the given bucket_path is not part of the currently opended
                filesystem.
        """
        with open_location(self._fsconfig) as (filesystem, path):
            return filesystem.cat(self.join_paths(path, bucket_path))

    def join_paths(self, *paths: str) -> str:
        """joins the given paths with the fsspec specific path seperator"""
        paths = [path for path in paths if len(path) > 0]
        with open_location(self._fsconfig) as (filesystem, _):
            return filesystem.sep.join(paths)

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
