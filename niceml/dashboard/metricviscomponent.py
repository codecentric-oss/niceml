"""Module for MetricVisComponent for the dashboard"""
from typing import List, Optional

import streamlit as st

from niceml.dashboard.components.expviscomponent import ExpVisComponent
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentmanager import ExperimentManager
from niceml.utilities.chartutils import generate_chart


class MetricVisComponent(ExpVisComponent):  # pylint: disable=too-few-public-methods
    """Dashboard ExpVisComponent to visualize all metrics
    in two columns (the right side starting with val_)"""

    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,  # pylint: disable=unused-argument
        exp_ids: List[str],
        subset_name: Optional[str] = None,  # pylint: disable=unused-argument
    ):
        metric_list = exp_manager.get_metrics(exp_ids)
        empty_exp_list: List[ExperimentData] = exp_manager.get_empty_exps(list(exp_ids))
        for exp in empty_exp_list:
            st.markdown(f"{exp.get_run_id()} - {exp.get_short_id()} is empty!")
        # Visualize in the center
        if not exp_ids:
            st.warning("No trained experiment selected!")
        else:
            chart_data_list = generate_charts_for_metrics(
                exp_ids, exp_manager, metric_list
            )
            cols = st.columns(2)
            for idx, chart_data in enumerate(chart_data_list):
                if (idx % 2) == 0:
                    cols[0].write(chart_data)
                else:
                    cols[1].write(chart_data)


def generate_charts_for_metrics(
    exp_ids: List[str], exp_manager: ExperimentManager, metric_list: List[str]
) -> list:
    """
    Generates all charts for selected experiments and metrics and caches them

    Args:
        exp_ids: Experiment Ids to get the metrics charts for
        exp_manager: Experiment Manager to get the data from
        metric_list: Metrics to get the charts of

    Returns:
        List of charts for each metric
    """

    @st.cache_data()
    def _get_metrics_charts(*args) -> list:  # pylint: disable = unused-argument
        """Generates all charts for selected experiments and metrics"""
        sorted_metrics = sort_metric_list(metric_list)
        chart_data_list = []
        for metric in sorted_metrics:
            cur_df = exp_manager.get_visu_df(metric, list(exp_ids))
            if cur_df is None:
                continue
            chart_data = generate_chart(cur_df, metric)
            chart_data_list.append(chart_data)
        return chart_data_list

    return _get_metrics_charts(exp_ids, metric_list)


def sort_metric_list(metric_list: List[str]) -> List[str]:
    """
    Sorts the metric list so that validation metrics are together with train metrics.

    Args:
        metric_list: List[str]: list of metrics

    Returns:
        A list of strings where the validation metrics are together with the train metrics

    """

    train_metrics = sorted([x for x in metric_list if not x.startswith("val_")])
    sorted_metrics = []
    for met in train_metrics:
        sorted_metrics.append(met)
        sorted_metrics.append(f"val_{met}")
    return sorted_metrics
