import os
import sys
from typing import List

import numpy as np
from hydra.utils import instantiate
from nicegui import ui

from niceml.dashboard.remotettrainutils import (
    exp_manager_factory,
    load_experiments,
    query_experiments,
    select_to_load_exps,
)
from niceml.data.storages.storagehandler import StorageHandler
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experimental.nicegui.ngfilter import NGFilterManager
from niceml.experimental.nicegui.ngframe import SiteRefs, NgFrameFactory
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.filters.experimentfilter import ExperimentFilter
from niceml.scripts.hydraconfreader import load_hydra_conf


class Dashboard:
    def __init__(self):
        self.exp_manager = None
        self.main_frame = None
        self.expdata_list = None
        self.exp_filter_list = None
        self.cloud_storage = None
        self.exp_cache = None
        self.ng_frame = None
        self.site_components = None
        self.site_refs = None
        self.config_instances = None

    def run_dashboard(self, config_instances: dict):
        self.config_instances = config_instances
        title = self.config_instances["title"]

        self.site_refs = [
            SiteRefs(elem.name, f"/{elem.name}")
            for elem in self.config_instances["pages"]
        ]

        self.site_components = {
            elem.name: elem.component for elem in self.config_instances["pages"]
        }
        home_ref = SiteRefs("Home", "/")
        self.site_refs.insert(0, home_ref)

        self.ng_frame = NgFrameFactory(title, self.site_refs)
        # here we use our custom page decorator directly and just put the content creation into a separate function

        storage_handler: StorageHandler = self.config_instances["storage_handler"]
        storage_handler_names: List[str] = storage_handler.get_storage_names()
        self.exp_cache = self.config_instances.get("exp_cache", None)
        storage_handler_name = storage_handler_names[1]

        self.cloud_storage: StorageInterface = storage_handler.get_storage(
            storage_handler_name
        )

        self.load_pages()

    def load_pages(self):
        self.main_frame = ui.column().classes("w-full")
        for site in self.site_refs:

            @ui.page(site.target)
            async def page(site=site):
                self.main_frame.clear()
                try:
                    self.component = self.site_components[site.name]
                    with self.ng_frame(site.name):
                        if self.expdata_list:
                            # Sidebar
                            with ui.left_drawer().props("width=330 bordered").classes(
                                "bg-[#eee]"
                            ):
                                ui.label("Select from the following filters:")
                                exp_filter_manager = NGFilterManager(
                                    self.exp_filter_list
                                )
                                exp_filter_manager.initialise(
                                    on_change_callback=self.on_change
                                )
                                exp_filter_manager.render(exp_list=self.expdata_list)

                            self.container = ui.column().classes("w-full")
                            self.container.clear()
                            self.render_main(self.expdata_list, self.component, False)
                        else:
                            ui.label(
                                'You have no experiments loaded, please head to the home page and press "Load experiments"'
                            )
                            self.loading_button_container = ui.row().classes("w-90")
                            self.loading_button_container.clear()
                            with self.loading_button_container:
                                ui.button(
                                    "Load Experiments",
                                    on_click=self.load_experiments_button,
                                )
                except:
                    home_frame = self.ng_frame("- Home -")
                    with home_frame:
                        ui.label("This is the home page.").classes(
                            "text-h4 font-bold text-grey-8"
                        )
                        self.generate_experiment_chart()

                        self.loading_button_container = ui.row().classes("w-90")
                        self.loading_button_container.clear()
                        with self.loading_button_container:
                            ui.button(
                                "Load Experiments",
                                on_click=self.load_experiments_button,
                            )

    def on_change(self, expdata_list):
        update = True
        self.render_main(
            expdata_list=expdata_list, component=self.component, update=update
        )

    def render_main(self, expdata_list, component, update):
        exp_id_list: List[str] = [x.exp_info.short_id for x in expdata_list]
        with self.container:
            component.render(
                self.exp_manager, self.cloud_storage, exp_id_list, update=update
            )

    async def load_experiments(self) -> None:
        self.exp_manager = exp_manager_factory(id(self.cloud_storage))
        exp_list: List[ExperimentInfo] = query_experiments(self.cloud_storage)
        exps_to_load = select_to_load_exps(exp_list, self.exp_manager)
        experiments = load_experiments(
            self.cloud_storage,
            exps_to_load,
            local_exp_cache=self.exp_cache,
            image_loader_factory=self.config_instances["image_loader_factory"],
            df_loader_factory=self.config_instances["df_loader_factory"],
        )
        for experiment in experiments:
            self.exp_manager.add_experiment(experiment)

        self.exp_filter_list: List[ExperimentFilter] = self.config_instances[
            "sidebar_filters"
        ]
        self.expdata_list: List[ExperimentData] = self.exp_manager.get_experiments()

        with self.loading_button_container:
            ui.icon("done", color="primary").classes("text-5xl")

        self.load_pages()

    async def load_experiments_button(self):
        await self.load_experiments()

    def generate_experiment_chart(self):
        experiment_list = np.array(
            [
                dir.split("-")[0]
                for dir in os.listdir("experiment_outputs")
                if dir[0] != "."
            ]
        )
        unique, counts = np.unique(experiment_list, return_counts=True)

        experiment_counts = dict(zip(unique, counts))

        ui.label(f"You have {len(experiment_list)} experiments in your list.")
        ui.highchart(
            {
                "title": False,
                "chart": {"type": "bar"},
                "xAxis": {"categories": "counts"},
                "series": [
                    {"name": key, "data": [experiment_counts[key]]}
                    for key in experiment_counts
                ],
            }
        ).classes("w-90 h-64")

        ui.echart(
            {
                "yAxis": {
                    "type": "category",
                    "data": [name for name in experiment_counts],
                },
                "xAxis": {"type": "value"},
                "series": [
                    {
                        "data": [value for value in experiment_counts.values()],
                        "type": "bar",
                        "showBackground": True,
                        "backgroundStyle": {"color": "rgba(180, 180, 180, 0.2)"},
                    }
                ],
            }
        ).classes("w-90 h-64")


def run_dashboard_with_confpath(config_path: str):
    """Runs the dashboard with the given config path"""
    config = load_hydra_conf(config_path)
    config_instances = instantiate(config)
    dashboard = Dashboard()
    dashboard.run_dashboard(config_instances)


if __name__ in {"__main__", "__mp_main__"}:
    arg_conf_path: str = sys.argv[1]
    run_dashboard_with_confpath(arg_conf_path)
    ui.run(favicon="🚀", show=False)
