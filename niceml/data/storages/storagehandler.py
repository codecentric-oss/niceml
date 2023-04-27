""" Handles multiple storages for the dashboard """
from typing import Dict, List

from niceml.data.storages.storageinterface import StorageInterface


class StorageNotAvailableError(Exception):
    """Error when the name of the storage is not declared"""


class StorageHandler:
    """Handles multiple storages for the dashboard"""

    def __init__(self, storages: Dict[str, StorageInterface]):
        self.storages = storages

    def get_storage_names(self) -> List[str]:
        """Returns a list of all storage names"""
        return list(self.storages.keys())

    def get_storage(self, name: str) -> StorageInterface:
        """Returns the storage with the given name"""
        try:
            return self.storages[name]
        except KeyError as error:
            raise StorageNotAvailableError(
                f"Storage with name: {name} not available!"
            ) from error
