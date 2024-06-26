"""Module for dataframe loaders"""
from os.path import isfile, join
from typing import Optional

import pandas as pd

from niceml.data.dataloaders.factories.dfloaderfactory import DfLoaderFactory
from niceml.data.dataloaders.interfaces.dfloader import DfLoader
from niceml.data.storages.localstorage import LocalStorage
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.loaddatafunctions import LoadParquetFile, LoadCsvFile
from niceml.utilities.ioutils import read_parquet, write_parquet, read_csv, write_csv


class SimpleDfLoader(DfLoader):  # pylint: disable=too-few-public-methods
    """SimpleLoader for parquet or csv files"""

    def __init__(
        self,
        storage: Optional[StorageInterface] = None,
        working_dir: Optional[str] = None,
    ):
        """SimpleLoader for parquet files"""

        self.storage = storage or LocalStorage()
        self.working_dir = working_dir

    def load_df(self, df_path: str, **kwargs) -> pd.DataFrame:
        """Loads and returns a dataframe from a given parquet or csv file path"""
        target_path = (
            self.storage.join_paths(self.working_dir, df_path)
            if self.working_dir
            else df_path
        )
        if ".parq" in target_path:
            return LoadParquetFile().load_data(target_path, self.storage)
        else:
            return LoadCsvFile().load_data(target_path, self.storage, **kwargs)


class SimpleDfLoaderFactory(DfLoaderFactory):  # pylint: disable=too-few-public-methods
    """SimpleLoader for parquet or csv files"""

    def create_df_loader(self, storage: StorageInterface, working_dir: str) -> DfLoader:
        """Returns SimpleDfLoader"""
        return SimpleDfLoader(storage, working_dir)


class RemoteDiskCachedDfLoader(DfLoader):  # pylint: disable=too-few-public-methods
    """SimpleLoader for parquet or csv files from cache or remote storage"""

    def __init__(
        self,
        storage: StorageInterface,
        cache_dir: str,
        working_dir: Optional[str] = None,
    ):
        """Initialize a SimpleLoader for parquet files from cache or remote storage"""
        self.storage = storage
        self.cache_path = cache_dir
        self.working_dir = working_dir

    def load_df(self, df_path: str, **kwargs) -> pd.DataFrame:
        """Loads and returns dataframe from cache"""
        target_path = (
            self.storage.join_paths(self.working_dir, df_path)
            if self.working_dir
            else df_path
        )
        cached_filepath = join(self.cache_path, target_path)
        if isfile(cached_filepath):
            if ".parq" in target_path:
                dataframe = read_parquet(cached_filepath)
            else:
                dataframe = read_csv(cached_filepath, **kwargs)
        elif ".parq" in target_path:
            dataframe = LoadParquetFile().load_data(target_path, self.storage)
            write_parquet(dataframe, cached_filepath)
        else:
            dataframe = LoadCsvFile().load_data(target_path, self.storage, **kwargs)
            write_csv(dataframe, cached_filepath, **kwargs)
        return dataframe


class RemoteDiskCachedDfLoaderFactory(
    DfLoaderFactory
):  # pylint: disable=too-few-public-methods
    """Factory of RemoteDiskCachedDfLoader"""

    def __init__(self, cache_dir: str):
        """Initialize a Factory for RemoteDiskCachedDfLoader"""

        self.cache_path = cache_dir

    def create_df_loader(self, storage: StorageInterface, working_dir: str) -> DfLoader:
        """Returns RemoteDiskCachedDfLoader"""
        return RemoteDiskCachedDfLoader(storage, self.cache_path, working_dir)
