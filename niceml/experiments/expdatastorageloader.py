"""Module for loading remote ExperimentData"""
from os.path import relpath, splitext
from typing import Any, Dict, List, Optional

import pandas as pd
from pandas.errors import EmptyDataError

from niceml.data.dataloaders.interfaces.dfloader import DfLoader
from niceml.data.dataloaders.interfaces.imageloader import ImageLoader
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.experiments.loaddatafunctions import (
    LoadCsvFile,
    LoadDataFunc,
    LoadParquetFile,
    LoadYamlFile,
)
from niceml.experiments.loadexpinfo import load_exp_info


def read_remote_data(
    exp_path: str,
    exp_files: List[str],
    storage: StorageInterface,
    extensions: List[str],
    load_data_func: LoadDataFunc,
) -> Dict[str, Any]:
    """
    Loads remote data and returns them in a dictionary with corresponding paths.

    Parameters
    ----------
    exp_path: str
        path to the experiment
    exp_files: List[str]
        all files which should be considered, absolute paths
    storage: StorageInterface
        interface to load data from cloud storage
    extensions: List[str]
        extension list to filter the files e.g. ['.yml', '.yaml']
    load_data_func: LoadDataFunc
        function to load the data
    Returns
    -------
    A dictionary with relative paths (without extension) to the data
    """
    load_files = [x for x in exp_files if splitext(x)[1] in extensions]
    global_dict = {}
    for cur_file in load_files:
        fname = relpath(splitext(cur_file)[0], exp_path)
        global_dict[fname] = load_data_func.load_data(cur_file, storage)
    return global_dict


def create_expdata_from_storage(
    exp_path: str,
    storage: StorageInterface,
    image_loader: Optional[ImageLoader] = None,
    df_loader: Optional[DfLoader] = None,
) -> ExperimentData:
    """Creates and loads an experiment data with the given path"""
    exp_info: ExperimentInfo = load_exp_info(storage, exp_path)
    try:
        exp_file_df: pd.DataFrame = LoadParquetFile().load_data(
            storage.join_paths(exp_path, ExperimentFilenames.EXP_FILES_FILE),
            storage,
        )
        exp_files: List[str] = exp_file_df[ExperimentFilenames.EXP_FILES_COL].tolist()
        exp_files = [storage.join_paths(exp_path, x) for x in exp_files]
    except (EmptyDataError, FileNotFoundError):
        exp_files = storage.list_data(exp_path)

    try:
        log_data: pd.DataFrame = LoadCsvFile().load_data(
            storage.join_paths(exp_path, ExperimentFilenames.TRAIN_LOGS),
            storage,
        )
    except (EmptyDataError, FileNotFoundError):
        log_data = pd.DataFrame()
    yaml_data = read_remote_data(
        exp_path, exp_files, storage, [".yaml", ".yml"], LoadYamlFile()
    )

    rel_exp_files = [relpath(x, exp_path) for x in exp_files]

    exp_data = ExperimentData(
        exp_path,
        exp_info=exp_info,
        log_data=log_data,
        exp_files=rel_exp_files,
        exp_dict_data=yaml_data,
        image_loader=image_loader,
        df_loader=df_loader,
    )
    return exp_data
