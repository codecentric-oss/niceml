"""Module for YamlFileLoaders"""
from os.path import join, isfile
from typing import Optional

from niceml.data.dataloaders.factories.fileloaderfactory import FileLoaderFactory
from niceml.data.dataloaders.interfaces.fileloader import FileLoader
from niceml.data.storages.localstorage import LocalStorage
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.loaddatafunctions import LoadYamlFile
from niceml.utilities.ioutils import read_yaml, write_yaml


class RemoteDiskCachedYamlFileLoader(FileLoader):
    """Remote Yaml file loader which creates cache data"""

    def __init__(
        self,
        storage: StorageInterface,
        cache_dir: str,
        working_dir: str,
    ):
        """Yaml file loader"""
        self.storage = storage
        self.cache_path = cache_dir
        self.working_dir = working_dir

    def load_file(self, file_path: str, **kwargs) -> dict:
        """Loads and returns dataframe from remote or cache"""
        target_path = (
            self.storage.join_paths(self.working_dir, file_path)
            if self.working_dir
            else file_path
        )
        cached_filepath = join(self.cache_path, target_path)
        if isfile(cached_filepath):
            yaml_dict = read_yaml(cached_filepath)
        else:
            yaml_dict = LoadYamlFile().load_data(target_path, self.storage)
            write_yaml(yaml_dict, cached_filepath)
        return yaml_dict


class RemoteDiskCachedYamlFileLoaderFactory(
    FileLoaderFactory
):  # pylint: disable=too-few-public-methods
    """Factory of RemoteDiskCachedYamlFileLoader"""

    def __init__(self, cache_dir: str):
        """Initialize a Factory for RemoteDiskCachedYamlFileLoader"""
        self.cache_path = cache_dir

    def create_file_loader(
        self, storage: StorageInterface, working_dir: str
    ) -> FileLoader:
        """Returns a RemoteDiskCachedYamlFileLoader"""
        return RemoteDiskCachedYamlFileLoader(storage, self.cache_path, working_dir)


class SimpleYamlFileLoader(FileLoader):
    """Simple Yaml file loader (e.g. for local files)"""

    def __init__(
        self,
        storage: Optional[StorageInterface] = None,
        working_dir: Optional[str] = None,
    ):
        """Yaml file loader"""
        self.storage = storage or LocalStorage()
        self.working_dir = working_dir

    def load_file(self, file_path: str, **kwargs) -> dict:
        """Loads and returns dataframe"""
        target_path = (
            self.storage.join_paths(self.working_dir, file_path)
            if self.working_dir
            else file_path
        )
        return LoadYamlFile().load_data(target_path, self.storage)


class SimpleYamlFileLoaderFactory(
    FileLoaderFactory
):  # pylint: disable=too-few-public-methods
    """Factory of SimpleYamlFileLoader"""

    def create_file_loader(
        self, storage: StorageInterface, working_dir: str
    ) -> FileLoader:
        """Returns a SimpleYamlFileLoader"""
        return SimpleYamlFileLoader(storage, working_dir)
