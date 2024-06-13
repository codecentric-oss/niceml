"""Module for FileLoaderFactory"""
from abc import ABC, abstractmethod

from niceml.data.dataloaders.interfaces.fileloader import FileLoader
from niceml.data.storages.storageinterface import StorageInterface


class FileLoaderFactory(ABC):  # pylint: disable=too-few-public-methods
    """Abstract implementation of FileLoaderFactory"""

    @abstractmethod
    def create_file_loader(
        self, storage: StorageInterface, working_dir: str
    ) -> FileLoader:
        """Creates a file loader"""
