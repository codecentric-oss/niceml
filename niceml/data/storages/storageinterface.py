from abc import ABC, abstractmethod
from typing import List, Optional

from niceml.experiments.experimentinfo import ExperimentInfo


class StorageInterface(ABC):
    """Interface for cloud storage access"""

    @abstractmethod
    def list_data(self, path: Optional[str] = None) -> List[str]:
        """Lists all files recursively from the given directory
        Returns absolute paths"""

    @abstractmethod
    def download_data(self, bucket_path: str, local_path: str):
        """Downloads the file from the bucket and stores it locally"""

    @abstractmethod
    def download_as_str(self, bucket_path: str) -> bytes:
        """Dowloads the file and returns it as byte string"""

    @abstractmethod
    def join_paths(self, *paths) -> str:
        """Joins the paths with the correct separator"""

    @abstractmethod
    def list_experiments(self, path: Optional[str] = None) -> List[ExperimentInfo]:
        """Lists all experiment infos of the given path"""
