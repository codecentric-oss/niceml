"""Module for FileLoader"""
from abc import ABC, abstractmethod
from typing import Union


class FileLoader(ABC):  # pylint: disable=too-few-public-methods
    """Abstract class DfLoader (Dataframe Loader)"""

    @abstractmethod
    def load_file(self, file_path: str, **kwargs) -> Union[str, dict, list]:
        """Loads and returns the content of the given file"""
