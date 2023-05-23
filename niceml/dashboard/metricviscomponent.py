"""module for metricviscomponent"""
from typing import List, Optional

import numpy as np
from nicegui import ui

from niceml.dashboard.components.expviscomponent import ExpVisComponent
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentmanager import ExperimentManager
from niceml.utilities.chartutils import Chart


class MetricVisComponent(ExpVisComponent):
    """ExpVisComponent to visualize all metrics
    in two columns (the right side starting with val_)"""

    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_ids: List[str],
        subset_name: Optional[str] = None,
        update: bool = False,
    ):
        metric_list = exp_manager.get_metrics(exp_ids)
        empty_exp_list: List[ExperimentData] = exp_manager.get_empty_exps(list(exp_ids))
        for exp in empty_exp_list:
            ui.markdown(f"{exp.get_run_id()} - {exp.get_short_id()} is empty!")

        # Visualize in the center
        if not exp_ids:
            raise OverflowError
        else:
            generate_charts(
                exp_ids,
                exp_manager,
                metric_list
            )


def generate_charts(
    exp_ids: List[str], exp_manager: ExperimentManager, metric_list: str
) -> None:
    """Generating all chart data with highchart in nicegui"""

    def _cached_chart_data(*args) -> None:
        cur_df = exp_manager.get_visu_df(metric, list(exp_ids))
        name_df = list(exp_ids)
        chart = Chart(
            cur_df.round(6),
            metric,
            name_df,
        )
        if cur_df is None:
            return
        chart.generate_chart()

    with ui.row().classes("w-full no-wrap"):
        col = [ui.column().classes("w-1/2") for _ in range(2)]

    for idx, metric in enumerate(metric_list):
        if (idx % 2) == 0:
            with col[idx % 2]:
                _cached_chart_data(exp_ids, metric)
        else:
            with col[idx % 2]:
                _cached_chart_data(exp_ids, metric)
