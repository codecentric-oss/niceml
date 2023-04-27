"""Module for DfLoaderFactory"""
from abc import ABC, abstractmethod

from niceml.data.dataloaders.interfaces.dfloader import DfLoader
from niceml.data.storages.storageinterface import StorageInterface


class DfLoaderFactory(ABC):  # pylint: disable=too-few-public-methods
    """Abstract implementation of DfLoaderFactory (Dataframe Loader Factory)"""

    @abstractmethod
    def create_df_loader(self, storage: StorageInterface, working_dir: str) -> DfLoader:
        """Creates a dataframe loader (DFLoader)"""
