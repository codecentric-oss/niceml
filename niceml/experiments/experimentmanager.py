"""Module for the experimentmanager"""
import logging
import os
from collections import defaultdict
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np
import pandas as pd

from niceml.experiments.expdatalocalstorageloader import (
    create_expdata_from_local_storage,
)
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimenterrors import (
    EmptyExperimentError,
    InfoNotFoundError,
    LogEmptyError,
)
from niceml.experiments.experimentinfo import ExperimentInfo


class ExperimentManager(object):
    """Class for managing experiments"""

    def __init__(self, experiments: List[ExperimentData] = None):
        """Manages a list of experiments"""
        self.experiments = [] if experiments is None else experiments
        self.exp_dict = {exp.get_short_id(): exp for exp in self.experiments}
        self.exp_dict.update({exp.get_run_id(): exp for exp in self.experiments})

    def add_experiment(self, experiment: ExperimentData):
        """Adds an experiment to the manager"""
        self.experiments.append(experiment)
        self.exp_dict[experiment.get_short_id()] = experiment
        self.exp_dict[experiment.get_run_id()] = experiment

    def __contains__(self, exp_id: Union[str, ExperimentInfo]):
        if type(exp_id) == ExperimentInfo:
            exp_id = exp_id.short_id
        for experiment in self.experiments:
            if exp_id.endswith(experiment.get_short_id()):
                return True
        return False

    def get_exp_count(self) -> int:
        """Returns the number of experiments"""
        return len(self.experiments)

    def get_exp_prefix(self, exp_id) -> str:
        """extracts the prefix from the target exp data"""
        exp_data: ExperimentData = self.get_exp_by_id(exp_id)
        return exp_data.exp_info.experiment_prefix

    def get_best_experiments(
        self, metric_name: str, mode: str, number_of_exps: int
    ) -> List[Tuple[str, ExperimentData]]:
        """
        Finds the best experiments according to given metric.
        Parameters
        ----------
        metric_name: str
            name of the metric
        mode: str
            use 'max' for maximum and 'min' for minimum values
        number_of_exps
            number of experiments which should be included
        Returns
        -------
            A list of Tuple[str, ExperimentData].
            The str is a readable representation of the value and the
            experiment id
        """
        if mode not in ["max", "min"]:
            raise Exception(f"mode is not max or min but : {mode}")
        exp_list = self.experiments
        number_of_exps = min(number_of_exps, len(exp_list))
        value_exps = [
            (exp, exp.get_best_metric_value(metric_name, mode))
            for exp in exp_list
            if exp.has_metric(metric_name)
        ]
        reversed = True if mode == "max" else False
        value_exps = sorted(value_exps, reverse=reversed, key=lambda x: x[1].value)
        value_exps = value_exps[:number_of_exps]

        return [
            (f"{exp.exp_info.short_id} - {value.value:0.2f}", exp)
            for exp, value in value_exps
        ]

    def get_metrics(self, experiments: Optional[List[str]] = None) -> List[str]:
        """Returns a list of all metrics used in the experiments"""
        metric_set: Set[str] = set()
        for cur_exp in self.experiments:
            if experiments is not None and cur_exp.get_short_id() not in experiments:
                continue
            metric_set.update(cur_exp.get_metrics())

        return sorted(list(metric_set))

    def get_datasets(self) -> List[str]:
        """Returns a list of all datasets used in the experiments"""
        dataset_set: Set[str] = set()
        for cur_exp in self.experiments:
            dataset_set.add(cur_exp.get_experiment_path().split("/")[0])

        return sorted(list(dataset_set))

    def get_experiment_type(self, experiment: ExperimentData) -> str:
        """Returns the experiment type of the given experiment"""
        return experiment.get_experiment_path().split("/")[-1].split("-")[0]

    def get_experiment_types(self) -> List[str]:
        """Returns a list of all experiment types"""
        experiment_type_set: Set[str] = set()
        for cur_exp in self.experiments:
            experiment_type_set.add(self.get_experiment_type(cur_exp))

        return sorted(list(experiment_type_set))

    def get_experiments(self) -> List[ExperimentData]:
        """Returns a sorted list of all experiments (newest first)"""
        return sorted(self.experiments, reverse=True, key=lambda x: x.get_run_id())

    def get_exp_by_id(self, exp_id: str) -> ExperimentData:
        """
        Returns the experiment with the given id

        Parameters
        ----------
        exp_id: str
            alphanumeric str with 4 digits of the desired experiment
            OR 'latest' for the newest experiment

        Returns
        -------
        experiment: ExperimentData

        Raises
        ------
        KeyError
            If the experiment id does not exist
        """
        if exp_id.lower() == "latest":
            ret_exp = sorted(
                self.experiments, reverse=True, key=lambda x: x.get_run_id()
            )[0]
        else:
            ret_exp = self.exp_dict[exp_id]
        return ret_exp

    def get_empty_exps(
        self, id_list: Optional[List[str]] = None
    ) -> List[ExperimentData]:
        """Finds all experiments which are empty"""
        if id_list is None:
            id_list = [x.get_short_id() for x in self.experiments]
        exp_list = [self.exp_dict[x] for x in id_list]
        empty_list = [x for x in exp_list if x.is_empty()]
        return empty_list

    def get_visu_df(self, metric_name: str, exp_id_list: List[str]) -> pd.DataFrame:
        """Returns a dataframe for the metric and experiments"""
        df = None
        for exp_id in exp_id_list:
            exp = self.get_exp_by_id(exp_id)
            try:
                cur_df = exp.get_log_for_metric(metric_name)
            except LogEmptyError:
                continue
            if df is None:
                df = cur_df
            else:
                df = pd.concat([df, cur_df])

        return df

    def get_metrics_visu_df(
        self, metric_names: List[str], exp_id_list: List[str]
    ) -> pd.DataFrame:
        """Returns a dataframe for the metrics visu, containing the min, max value for
        each metric and each experiment"""
        mode_dict: Dict[str, str] = {
            "accuracy": "max",
            "loss": "min",
            "iou": "max",
            "precision": "max",
            "recall": "max",
        }
        metrics_data = pd.DataFrame()
        for met in metric_names:
            if not met.startswith("val_"):
                val_met = f"val_{met}"
                cur_df = self.get_visu_df(met, list(exp_id_list))
                cur_val_df = self.get_visu_df(val_met, list(exp_id_list))
                if cur_df is None or cur_val_df is None:
                    continue
                min_met = []
                min_val_met = []
                max_met = []
                max_val_met = []
                experiment_names = []
                for experiment in list(exp_id_list):
                    experiment_names.append(experiment)
                    experiment_df = cur_df[cur_df["name"] == experiment]
                    experiment_val_df = cur_val_df[cur_val_df["name"] == experiment]
                    if experiment_df.empty or experiment_val_df.empty:
                        if experiment_df.empty:
                            min_met.append(np.nan)
                            max_met.append(np.nan)
                        if experiment_val_df.empty:
                            min_val_met.append(np.nan)
                            max_val_met.append(np.nan)
                        continue
                    min_met.append(min(cur_df[cur_df["name"] == experiment][met]))
                    max_met.append(max(cur_df[cur_df["name"] == experiment][met]))
                    min_val_met.append(
                        min(cur_val_df[cur_val_df["name"] == experiment][val_met])
                    )
                    max_val_met.append(
                        max(cur_val_df[cur_val_df["name"] == experiment][val_met])
                    )
                metrics_data["Experiment"] = experiment_names
                add_min, add_max = get_add_min_max(met, mode_dict)
                if add_min:
                    metrics_data[f"{met}_min"] = min_met
                    metrics_data[f"{val_met}_min"] = min_val_met
                if add_max:
                    metrics_data[f"{met}_max"] = max_met
                    metrics_data[f"{val_met}_max"] = max_val_met
        return metrics_data

    def get_value_information_dict(
        self, info_path: List[str], list_connection_str: str = "x"
    ) -> Dict[Any, List[str]]:
        value_information_dict = defaultdict(list)
        for exp in self.experiments:
            try:
                exp_info = exp.get_config_information(info_path)
                if type(exp_info) is list:
                    exp_info = list_connection_str.join([str(x) for x in exp_info])
                value_information_dict[exp_info].append(exp.exp_info.short_id)
            except InfoNotFoundError:
                pass

        return value_information_dict

    def get_epochs_information_dict(self) -> Dict[int, List[str]]:
        """Returns a dict with information about the trained epochs"""
        epochs_information_dict = defaultdict(list)
        for exp in self.experiments:
            epochs_information_dict[exp.get_trained_epochs()].append(exp.get_short_id())
        return epochs_information_dict

    def get_datasets_information_dict(self) -> Dict[str, List[str]]:
        datasets_information_dict = defaultdict(list)
        for exp in self.experiments:
            dataset = exp.get_experiment_path().split("/")[0]
            datasets_information_dict[dataset].append(exp.get_short_id())
        return datasets_information_dict

    def get_dataset(self, exp: ExperimentData) -> str:
        dataset = exp.get_experiment_path().split("/")[0]
        return dataset

    def get_date_information_dict(self) -> Dict[date, List[str]]:
        date_information_dict = defaultdict(list)
        for exp in self.experiments:
            date_string = exp.exp_info.run_id.split("T")[0]
            date = datetime.strptime(date_string, "%Y-%m-%d").date()
            date_information_dict[date].append(exp.get_short_id())
        return date_information_dict

    def get_experiment_type_information_dict(self) -> Dict[str, List[str]]:
        experiment_type_information_dict = defaultdict(list)
        for exp in self.experiments:
            experiment_type = exp.get_experiment_path().split("/")[-1].split("-")[0]
            experiment_type_information_dict[experiment_type].append(exp.get_short_id())
        return experiment_type_information_dict

    def get_max_trained_epochs(self) -> int:
        """Returns the max epochs of all trained experiments"""
        max_epochs = 0
        for exp in self.experiments:
            max_epochs = max(max_epochs, exp.get_trained_epochs())
        return max_epochs


def local_exp_manager_factory(path: str) -> ExperimentManager:
    """Creates a local experiment manager"""
    experiments: List[ExperimentData] = []
    for path in [f.path for f in os.scandir(path) if f.is_dir()]:
        try:
            experiments.append(create_expdata_from_local_storage(path))
        except EmptyExperimentError:
            logging.getLogger(__name__).info(f"Empty Experiment at: {path}")

    return ExperimentManager(experiments)


def get_add_min_max(metric_name: str, mode_dict: Dict[str, str]) -> Tuple[bool, bool]:
    add_min: bool = True
    add_max: bool = True
    for key, mode in mode_dict.items():
        if key in metric_name:
            if mode == "max":
                add_min = False
            if mode == "min":
                add_max = False
    return add_min, add_max
