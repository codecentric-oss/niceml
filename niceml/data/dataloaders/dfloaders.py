"""Module for dataframe loaders"""
from os.path import isfile, join
from typing import Optional

import pandas as pd

from niceml.data.dataloaders.factories.dfloaderfactory import DfLoaderFactory
from niceml.data.dataloaders.interfaces.dfloader import DfLoader
from niceml.data.storages.localstorage import LocalStorage
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.loaddatafunctions import LoadParquetFile
from niceml.utilities.ioutils import read_parquet, write_parquet


class SimpleDfLoader(DfLoader):  # pylint: disable=too-few-public-methods
    """SimpleLoader for parquet files"""

    def __init__(
        self,
        storage: Optional[StorageInterface] = None,
        working_dir: Optional[str] = None,
    ):
        self.storage = storage or LocalStorage()
        self.working_dir = working_dir

    def load_df(self, df_path: str) -> pd.DataFrame:
        """Loads and returns a dataframe from a given parquet file path"""
        target_path = join(self.working_dir, df_path) if self.working_dir else df_path
        return LoadParquetFile().load_data(target_path, self.storage)


class SimpleDfLoaderFactory(DfLoaderFactory):  # pylint: disable=too-few-public-methods
    """SimpleLoader for parquet files"""

    def create_df_loader(self, storage: StorageInterface, working_dir: str) -> DfLoader:
        """Returns SimpleDfLoader"""
        return SimpleDfLoader(storage, working_dir)


class RemoteDiskCachedDfLoader(DfLoader):  # pylint: disable=too-few-public-methods
    """SimpleLoader for parquet files from cache or remote storage"""  # QUEST: check docstring

    def __init__(
        self,
        storage: StorageInterface,
        cache_dir: str,
        working_dir: Optional[str] = None,
    ):
        self.storage = storage
        self.cache_path = cache_dir
        self.working_dir = working_dir

    def load_df(self, df_path: str) -> pd.DataFrame:
        """Loads and returns dataframe from cache"""
        target_path = (
            self.storage.join_paths(self.working_dir, df_path)
            if self.working_dir
            else df_path
        )
        cached_filepath = join(self.cache_path, target_path)
        if isfile(cached_filepath):
            dataframe = read_parquet(cached_filepath)
        else:
            dataframe = LoadParquetFile().load_data(target_path, self.storage)
            write_parquet(dataframe, cached_filepath)
        return dataframe


class RemoteDiskCachedDfLoaderFactory(  # QUEST: still used?
    DfLoaderFactory
):  # pylint: disable=too-few-public-methods
    """Factory of RemoteDiskCachedDfLoader"""

    def __init__(self, cache_dir: str):
        self.cache_path = cache_dir

    def create_df_loader(self, storage: StorageInterface, working_dir: str) -> DfLoader:
        """Returns RemoteDiskCachedDfLoader"""
        return RemoteDiskCachedDfLoader(storage, self.cache_path, working_dir)
