"""Module for helper functions for io operations"""
import json
from os.path import dirname, join, relpath, splitext
from typing import List, Optional, Any, Tuple

import fastparquet
import pandas as pd
import yaml
from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from PIL import Image

from niceml.utilities.fsspec.locationutils import join_fs_path


def list_dir(
    path: str,
    return_full_path: bool = False,
    recursive: bool = False,
    file_system: Optional[AbstractFileSystem] = None,
    filter_ext: Optional[List[str]] = None,
) -> List[str]:
    """
    Returns a list of files in a directory

    Args:
        path: path to directory, which should be listed
        return_full_path: Returns full filepaths (True) or relative path (False)
        recursive: Determine if the function should look into subfolders
        file_system: Allow the function to be used with different file systems; default = local

    Returns:
        A list of files in the specified directory
    """
    cur_fs: AbstractFileSystem = file_system or LocalFileSystem()
    files: List[str] = [
        relpath(cur_file, path) for cur_file in list(cur_fs.listdir(path, detail=False))
    ]
    if filter_ext is not None:
        files = [cur_file for cur_file in files if splitext(cur_file)[1] in filter_ext]
    if recursive:
        folders = [
            cur_folder for cur_folder in files if cur_fs.isdir(join(path, cur_folder))
        ]
        for cur_folder in folders:
            files += [
                join(cur_folder, cur_file)
                for cur_file in list_dir(
                    join(path, cur_folder), False, True, file_system=cur_fs
                )
            ]

    if return_full_path:
        files = [join(path, cur_file) for cur_file in files]

    return files


def write_parquet(
    dataframe: pd.DataFrame,
    filepath: str,
    compression: Optional[str] = "gzip",
    file_system: Optional[AbstractFileSystem] = None,
    **kwargs,
):
    """
    Writes dataframe to parquet file with optional AbstractFileSystem given

    Args:
        dataframe: Dataframe to write to parquet file
        filepath: Path to save the parquet file to
        compression: Compression method
        file_system: Allow the function to be used with different file systems; default = local
        **kwargs: additional arguments for fastparquet.write function
    """
    cur_fs: AbstractFileSystem = file_system or LocalFileSystem()
    cur_fs.mkdirs(
        dirname(filepath),
        exist_ok=True,
    )
    fastparquet.write(
        filepath,
        dataframe,
        open_with=cur_fs.open,
        compression=compression,
        **kwargs,
    )


def read_parquet(
    filepath: str, file_system: Optional[AbstractFileSystem] = None
) -> pd.DataFrame:
    """
    Reads parquet with optional AbstractFileSystem given

    Args:
        filepath: path to parquet file
        file_system: Allow the function to be used with different file systems; default = local

    Returns:
        dataframe from parquet file
    """
    cur_fs: AbstractFileSystem = file_system or LocalFileSystem()
    if not cur_fs.exists(filepath):
        raise FileNotFoundError(f"Parquetfile not found: {filepath}")
    return fastparquet.ParquetFile(filepath, fs=cur_fs).to_pandas()


def read_yaml(filepath: str, file_system: Optional[AbstractFileSystem] = None) -> dict:
    """
    Reads a yaml file with optional AbstractFileSystem given

    Args:
        filepath: path to yaml file
        file_system: Allow the function to be used with different file systems; default = local

    Returns:
        Content of yaml as dictionary
    """
    cur_fs: AbstractFileSystem = file_system or LocalFileSystem()
    if not cur_fs.exists(filepath):
        raise FileNotFoundError(f"Yamlfile not found: {filepath}")
    with cur_fs.open(filepath, "r", encoding="utf-8") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


def write_yaml(
    data: dict,
    filepath: str,
    file_system: Optional[AbstractFileSystem] = None,
    **kwargs,
):
    """
    Writes dictionary to yaml with optional AbstractFileSystem given

    Args:
        data: dictionary to be saved as yaml
        filepath: path to save the yaml file to
        file_system: Allow the function to be used with different file systems; default = local
        **kwargs: additional arguments for yaml.dump function
    """
    cur_fs: AbstractFileSystem = file_system or LocalFileSystem()
    cur_fs.mkdirs(
        dirname(filepath),
        exist_ok=True,
    )
    with cur_fs.open(filepath, "w", encoding="utf-8") as file:
        yaml.dump(data, file, Dumper=yaml.SafeDumper, **kwargs)


def read_json(filepath: str, file_system: Optional[AbstractFileSystem] = None) -> dict:
    """
    Reads a json file with optional AbstractFileSystem given

    Args:
        filepath: path to json file
        file_system: Allow the function to be used with different file systems; default = local

    Returns:
        Content of json as dictionary
    """
    cur_fs: AbstractFileSystem = file_system or LocalFileSystem()
    if not cur_fs.exists(filepath):
        raise FileNotFoundError(f"Yamlfile not found: {filepath}")
    with cur_fs.open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(
    data: dict,
    filepath: str,
    file_system: Optional[AbstractFileSystem] = None,
    **kwargs,
):
    """
    Writes dictionary to json with optional AbstractFileSystem given

    Args:
        data: dictionary to be saved as json
        filepath: path to save the json file to
        file_system: Allow the function to be used with different file systems; default = local
        **kwargs: additional arguments for json.dump function
    """
    cur_fs: AbstractFileSystem = file_system or LocalFileSystem()
    cur_fs.mkdirs(
        dirname(filepath),
        exist_ok=True,
    )
    with cur_fs.open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, **kwargs)


def write_csv(
    data: pd.DataFrame,
    filepath: str,
    file_system: Optional[AbstractFileSystem] = None,
    **kwargs,
):
    """
    Writes dataframe to csv file with optional AbstractFileSystem given

    Args:
        data: Dataframe to write to csv file
        filepath: Path to save the csv file to
        file_system: Allow the function to be used with different file systems; default = local
        **kwargs: additional arguments for data.to_csv function
    """
    cur_fs: AbstractFileSystem = file_system or LocalFileSystem()
    cur_fs.mkdirs(
        dirname(filepath),
        exist_ok=True,
    )
    with cur_fs.open(filepath, "w", encoding="utf-8") as file:
        data.to_csv(file, index=False, **kwargs)


def read_csv(
    filepath: str, file_system: Optional[AbstractFileSystem] = None, **kwargs
) -> pd.DataFrame:
    """Reads csv with optional AbstractFileSystem given

    Args:
        filepath: path to csv file
        file_system: Allow the function to be used with different file systems; default = local
        ***kwargs: additional arguments for pd.read_csv function

    Returns:
        dataframe from csv file"""
    cur_fs: AbstractFileSystem = file_system or LocalFileSystem()
    if not cur_fs.exists(filepath):
        raise FileNotFoundError(f"CSV not found: {filepath}")
    with cur_fs.open(filepath, "r", encoding="utf-8") as file:
        return pd.read_csv(file, **kwargs)


def write_image(
    image: Image.Image,
    filepath: str,
    file_system: Optional[AbstractFileSystem] = None,
    **kwargs,
):
    """
    Saves image to filepath with optional AbstractFileSystem given

    Args:
        image: Image object
        filepath: Path to save the image to
        file_system: Allow the function to be used with different file systems; default = local
        **kwargs: additional arguments for Image.save function
    """
    cur_fs: AbstractFileSystem = file_system or LocalFileSystem()
    cur_fs.mkdirs(
        dirname(filepath),
        exist_ok=True,
    )
    with file_system.open(filepath, "wb") as file:
        file_format = filepath.rsplit(".")[-1]
        image.save(file, format=file_format, **kwargs)


def read_image(
    filepath: str, file_system: Optional[AbstractFileSystem] = None, **kwargs
) -> Image.Image:
    """Reads image with optional AbstractFileSystem given

    Args:
        filepath: Path to load the image from
        file_system: Allow the function to be used with different file systems; default = local
        **kwargs: additional arguments for Image.open function

    Returns:
        loaded image object
    """
    cur_fs: AbstractFileSystem = file_system or LocalFileSystem()
    if not cur_fs.exists(filepath):
        raise FileNotFoundError(f"ImageFile not found: {filepath}")
    with file_system.open(filepath, "rb") as file:
        return Image.open(file, **kwargs).copy()


def find_and_read_file(
    filepath: str,
    read_func,
    search_paths: Optional[List[str]] = None,
    file_system: Optional[AbstractFileSystem] = None,
    **kwargs,
) -> Tuple[str, Any]:
    """
    Tries to find a file in a list of search paths and reads it with given read function

    Args:
        filepath: path to file
        search_paths: list of paths to search for file
        read_func: function to read the file
        file_system: Allow the function to be used with different file systems; default = local

    Returns:
        Content of file
    """
    cur_fs: AbstractFileSystem = file_system or LocalFileSystem()
    search_paths = search_paths or []
    if cur_fs.exists(filepath):
        return filepath, read_func(filepath, file_system=cur_fs, **kwargs)
    for path in search_paths:
        cur_path = join_fs_path(cur_fs, path, filepath)
        if cur_fs.exists(cur_path):
            return cur_path, read_func(cur_path, file_system=cur_fs, **kwargs)
    raise FileNotFoundError(f"File not found: {filepath}")
