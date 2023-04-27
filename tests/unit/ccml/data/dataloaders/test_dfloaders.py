import os
from os.path import isfile, join
from tempfile import TemporaryDirectory

import pandas as pd
import pytest

from niceml.data.dataloaders.dfloaders import RemoteDiskCachedDfLoader, SimpleDfLoader
from niceml.data.storages.localstorage import LocalStorage
from niceml.utilities.ioutils import write_parquet


@pytest.fixture()
def example_df():
    return pd.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": [4, 5, 6],
            "col3": [7, 8, 9],
        }
    )


@pytest.fixture()
def tmp_folder_with_parquet(example_df):
    with TemporaryDirectory() as tmpdir:
        write_parquet(example_df, join(tmpdir, "test.parquet"))
        yield tmpdir


@pytest.fixture()
def tmp_cache_dir() -> str:
    with TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_simple_df_loader(tmp_folder_with_parquet: str, example_df: pd.DataFrame):
    df_loader = SimpleDfLoader()
    df_test = df_loader.load_df(join(tmp_folder_with_parquet, "test.parquet"))
    assert isinstance(df_test, pd.DataFrame)
    assert df_test.equals(example_df)


def test_remote_disk_cached_df_loader(
    tmp_folder_with_parquet: str, example_df: pd.DataFrame, tmp_cache_dir: str
):
    storage = LocalStorage(tmp_folder_with_parquet)
    df_loader = RemoteDiskCachedDfLoader(storage, tmp_cache_dir)
    df_test = df_loader.load_df("test.parquet")
    assert isinstance(df_test, pd.DataFrame)
    assert df_test.equals(example_df)
    assert isfile(join(tmp_cache_dir, "test.parquet"))

    # remove file from orig folder to test if it is loaded from cache
    os.remove(join(tmp_folder_with_parquet, "test.parquet"))

    df_test = df_loader.load_df("test.parquet")
    assert isinstance(df_test, pd.DataFrame)
    assert df_test.equals(example_df)
