"""Module for experimentdata"""
import datetime
from dataclasses import dataclass
from os.path import basename, dirname, join, splitext
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from hydra.utils import instantiate
from isodate import parse_datetime

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.dataloaders.interfaces.dfloader import DfLoader
from niceml.data.dataloaders.interfaces.imageloader import ImageLoader
from niceml.experiments.experimenterrors import (
    AmbigousFilenameError,
    InfoNotFoundError,
    LogEmptyError,
    ModelNotFoundError,
)
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.utilities.commonutils import check_instance, human_readable_size


def load_loggings(logging_file: str) -> pd.DataFrame:
    """loads loggings from csv file"""
    return pd.read_csv(logging_file)


@dataclass
class MetricValue:
    """abstact implementation of MetricValue"""

    metric_name: str
    value: float
    epoch: int


class ExperimentData:  # pylint: disable = too-many-public-methods, too-many-instance-attributes
    """Implementation of Experiment Information"""

    def __init__(  # pylint: disable = too-many-arguments
        self,
        dir_name: str,
        exp_info: ExperimentInfo,
        exp_dict_data: dict,
        log_data: pd.DataFrame,
        exp_files: List[str],
        exp_tests: Optional[pd.DataFrame] = None,
        image_loader: Optional[ImageLoader] = None,
        df_loader: Optional[DfLoader] = None,
    ):
        self.dir_name = dir_name
        self.exp_info: ExperimentInfo = exp_info
        self.log_data = log_data
        self.all_exp_files: List[str] = exp_files
        self.exp_dict_data: Dict[str, Any] = exp_dict_data
        self.exp_tests: Optional[pd.DataFrame] = exp_tests
        self.image_loader: Optional[ImageLoader] = image_loader
        self.df_loader: Optional[DfLoader] = df_loader

    def __repr__(self) -> str:
        ret_str = f"ExpData:id_{self.get_short_id()}_{self.get_run_date().date()}"
        return ret_str

    def get_all_model_files(self) -> List[str]:
        """get list of all model files"""
        model_files = sorted(
            [
                x
                for x in self.all_exp_files
                if ExperimentFilenames.MODELS_FOLDER == basename(dirname(x))
            ]
        )
        return model_files

    def get_run_id(self) -> str:
        """get id of experiment run"""
        return self.exp_info.run_id

    def get_short_id(self) -> str:
        """get short id of experiment run"""
        return self.exp_info.short_id

    def get_run_date(self) -> datetime.datetime:
        """get date of experiment run"""
        return parse_datetime(self.get_run_id())

    def get_exp_prefix(self) -> str:
        """get prefix of experiment"""
        return self.exp_info.experiment_prefix

    def get_metrics(self) -> List[str]:
        """get experiment metrics"""
        metrics = list(self.log_data.columns)
        try:
            metrics.remove("epoch")
            metrics.remove("Unnamed: 0")
        except ValueError:
            pass
        return metrics

    def has_metric(self, metric_name: str) -> bool:
        """checks if given metric is available for the experiment run"""
        return metric_name in self.get_metrics()

    def get_rel_file_exp_path(self, file: str) -> str:
        """
        Returns the filepath of the given file relative to the experiment folder.
        Parameters
        ----------
        file: str
            Relative path from the experiment without or with extension.
            If the name is unique its enough to specify the basename of the file.
        Returns
        -------
        str: filepath of the dataframe file
        """
        if file in self.all_exp_files:
            return file
        file_name, file_ext = splitext(file)
        if file_ext == "":
            target_files = self.all_exp_files
        else:
            target_files = [x for x in self.all_exp_files if file_ext == splitext(x)[1]]

        matching_files = [
            x for x in target_files if basename(file_name) == basename(splitext(x)[0])
        ]
        if len(matching_files) == 0:
            raise FileNotFoundError(f"loaded_df: {self.get_short_id()} - {file}")
        if len(matching_files) == 1:
            return matching_files[0]
        raise AmbigousFilenameError(
            f"Multiple files are matching: {file}, "
            f"{matching_files}, expid: {self.get_short_id()}"
        )

    def load_df(self, file: str) -> pd.DataFrame:
        """
        Loads a dataframe file
        Parameters
        ----------
        file: str
            Relative path from the experiment without extension.
            If the name is unique its enough to specify the basename of the file.
        Returns
        -------
        pd.DataFrame: dataframe
        """
        file_path = self.get_rel_file_exp_path(file)
        if self.df_loader is None:
            raise Exception("No df loader is set")
        return self.df_loader.load_df(file_path)

    def get_loaded_yaml(self, file: str) -> Union[dict, list]:
        """gets a loaded yaml file"""
        if splitext(file)[1] in [".yaml", ".yml"]:
            file = splitext(file)[0]
        if file in self.exp_dict_data:
            return self.exp_dict_data[file]
        matching_files = [x for x in self.exp_dict_data.keys() if file == basename(x)]
        if len(matching_files) == 0:
            raise FileNotFoundError(f"loaded_yaml: {self.get_short_id()} - {file}")
        if len(matching_files) == 1:
            return self.exp_dict_data[matching_files[0]]
        raise AmbigousFilenameError(
            f"Multiple files are matching: {file}, "
            f"{matching_files}, expid: {self.get_short_id()}"
        )

    def get_in_memory_usage(self) -> str:
        """get memory usage of experiment"""
        return human_readable_size(self)

    def get_instantiated_data_description(
        self, class_renamings: Optional[Dict[str, str]] = None
    ) -> DataDescription:
        """Instantiates the DataDescription stored with the experiment
        If the name of the class has changed meanwhile, you can specify this in the class_renamings
        """
        class_renamings = class_renamings or {}
        data_description_yaml = self.get_config_information(["data_description"])
        cur_target = data_description_yaml["_target_"]
        data_description_yaml["_target_"] = class_renamings.get(cur_target, cur_target)
        data_description = instantiate(data_description_yaml)
        return check_instance(data_description, DataDescription)

    def get_log_for_metric(self, metric_name: str) -> pd.DataFrame:
        """Returns log information for given metric"""
        series_epoch = self._get_epoch_series()
        try:
            series_metrics = self.log_data[metric_name]
        except KeyError as error:
            raise LogEmptyError(
                f"Log of experiment is empty: {self.exp_info.short_id}"
            ) from error
        series_name = pd.Series(data=[self.exp_info.short_id] * len(series_epoch))
        log_data = pd.DataFrame(
            {"epoch": series_epoch, metric_name: series_metrics, "name": series_name}
        )

        return log_data

    def _get_epoch_series(self):
        try:
            series_epoch = self.log_data["epoch"]
        except KeyError as error:
            raise LogEmptyError(
                f"Log of experiment is empty: {self.exp_info.short_id}"
            ) from error
        return series_epoch

    def get_trained_epochs(self) -> int:
        """Uses the logfile to determine how many epochs have been trained"""
        try:
            epochs = len(self._get_epoch_series())
        except LogEmptyError:
            epochs = 0
        return epochs

    def is_empty(self) -> bool:
        """Determines whether the exp has trained epochs"""
        return self.get_trained_epochs() == 0

    def get_config_information(self, info_path: List[str]) -> Any:
        """
        Returns the information of the config (e.g. the input_image_size)
        The whole path of the information must be given:
        info_path = ["datasets", "data_description", "input_image_size"]
        """
        config_dict: Dict[str, Any] = self.get_config_dict()
        cur_info_path = info_path.copy()
        file = cur_info_path.pop(0)
        sub_config_dict = {
            key: value for key, value in config_dict.items() if file in key
        }
        if len(sub_config_dict) == 1:
            return extract_info_from_dict(
                list(sub_config_dict.values())[0], cur_info_path
            )
        if len(sub_config_dict) > 1:
            exact_sub_config_dict = {
                key: value
                for key, value in sub_config_dict.items()
                if file == basename(key)
            }
            if len(exact_sub_config_dict) == 1:
                return extract_info_from_dict(
                    list(exact_sub_config_dict.values())[0], cur_info_path
                )
        raise InfoNotFoundError(
            f"Information: {info_path} not found at {info_path[0]} in {self.exp_info.short_id}"
        )

    def get_config_dict(self) -> Dict[str, Any]:
        """Returns the config dict from the exp_dict_data"""
        config_dict = {
            key: value
            for key, value in self.exp_dict_data.items()
            if key.startswith(ExperimentFilenames.CONFIGS_FOLDER)
        }
        return config_dict

    def get_yaml_information(self, info_path: List[str]):
        """get info from yaml file at given info_path"""
        cur_info_path = info_path.copy()
        file = cur_info_path.pop(0)
        sub_info_dict = {
            key: value for key, value in self.exp_dict_data.items() if file in key
        }
        if len(sub_info_dict) == 1:
            return extract_info_from_dict(
                list(sub_info_dict.values())[0], cur_info_path
            )
        raise InfoNotFoundError(
            f"Information: {info_path} not found at {info_path[0]} in {self.exp_info.short_id}"
        )

    def get_best_metric_value(self, metric_name: str, mode) -> MetricValue:
        """
        Returns the best value of the given metric according to the mode.
        :param metric_name: name of the metric
        :param mode: either 'min' or 'max'
        :return: MetricValue
        """
        series_epoch = self._get_epoch_series()
        series_metrics = self.log_data[metric_name]
        if mode == "max":
            idx = np.argmax(series_metrics)
        elif mode == "min":
            idx = np.argmin(series_metrics)
        else:
            raise Exception(f"Mode is neither 'max' nor 'min' but {mode}")

        val = series_metrics[idx]
        epoch = series_epoch[idx]
        return MetricValue(metric_name=metric_name, value=val, epoch=epoch)

    def get_model_path(self, epoch: int = None, relative_path: bool = True) -> str:
        """
        Get the model path for the desired model.
        :param epoch: epoch as int if not given the latest is returned
        """
        ret_model = None
        model_files = self.get_all_model_files()
        if len(model_files) == 0:
            raise ModelNotFoundError(
                f"No model found for this experiment: {self.exp_info.short_id}"
            )

        if epoch is None:
            ret_model = model_files[-1]
        else:
            ep_str = ExperimentFilenames.EPOCHS_FORMATTING.format(epoch)
            for model_files in model_files:
                if ep_str in model_files:
                    ret_model = model_files

        if ret_model is None:
            raise ModelNotFoundError(
                f"Model from epoch: {epoch} not found in exp: "
                f"{self.exp_info.short_id}"
            )

        if relative_path:
            return ret_model

        return join(self.exp_info.exp_filepath, ret_model)

    def get_experiment_path(self):
        """get path to experiment"""
        return self.exp_info.exp_filepath

    def get_prediction_path(self) -> str:
        """get path to prediction folder"""
        return join(self.get_experiment_path(), ExperimentFilenames.PREDICTION_FOLDER)

    def get_analysis_path(self) -> str:
        """get path to analysis folder"""
        return join(self.get_experiment_path(), ExperimentFilenames.ANALYSIS_FOLDER)

    def set_loaders(
        self,
        *,
        df_loader: Optional[DfLoader] = None,
        image_loader: Optional[ImageLoader] = None,
    ):
        """set loaders for experiment"""
        if df_loader is not None:
            self.df_loader = check_instance(df_loader, DfLoader)
        if image_loader is not None:
            self.image_loader = check_instance(image_loader, ImageLoader)

    def get_file_paths(
        self, subfolder_name: str, suffix: Union[str, List[str]]
    ) -> List[str]:
        """
        Get a list of files in a subfolder with a specified `suffix`
        Args:
            subfolder_name: Name of the subfolder
            suffix: Suffix or list of suffixes that must be part of the file path to be returned

        Returns:
            list of filepaths as strings

        """

        filtered_paths = [
            file_paths
            for file_paths in self.all_exp_files
            if subfolder_name in file_paths
        ]
        if isinstance(suffix, str):
            suffix = [suffix]
        return [
            join(self.exp_info.exp_filepath, filtered_path)
            for filtered_path in filtered_paths
            if any(ext in filtered_path for ext in suffix)
        ]

    def __eq__(self, other: "ExperimentData") -> bool:
        """check if two experiments are equal"""
        exp_info_equal = self.exp_info == other.exp_info
        exp_dict_data_equal = self.exp_dict_data == other.exp_dict_data
        has_file_list = [
            cur_file in other.all_exp_files
            for cur_file in self.all_exp_files
            if "." in basename(cur_file)
        ]
        same_dir_name = self.dir_name == other.dir_name
        return (
            all(has_file_list)
            and exp_info_equal
            and exp_dict_data_equal
            and same_dir_name
        )


def extract_info_from_dict(info: dict, info_path: List[Union[str, int]]) -> Any:
    """Extracts information from a dict at given path"""
    for key in info_path:
        try:
            info = info[key]
        except (IndexError, KeyError) as excep:
            raise InfoNotFoundError(
                f"Information: {info_path} not found at {key}"
            ) from excep
    return info
