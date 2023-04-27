"""Module to run the dashboard"""
import sys
from typing import List

import streamlit as st
from hydra.core.global_hydra import GlobalHydra
from hydra.utils import instantiate

from niceml.dashboard.remotettrainutils import (
    exp_manager_factory,
    load_experiments,
    query_experiments,
    select_to_load_exps,
)
from niceml.data.storages.storagehandler import StorageHandler
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.filters.experimentfilter import ExperimentFilter
from niceml.scripts.hydraconfreader import load_hydra_conf


def cached_instantiate(hydra_conf):
    """Instantiate using hydra instantiate with a streamlit cache"""
    GlobalHydra.instance().clear()
    return instantiate(hydra_conf)


def run_dashboard(conf_instances):
    """Runs the dashboard with already loaded configs"""
    storage_handler: StorageHandler = conf_instances["storage_handler"]
    st.sidebar.title(conf_instances["title"])
    handler_name = st.sidebar.selectbox(
        "StorageName", storage_handler.get_storage_names()
    )
    storage: StorageInterface = storage_handler.get_storage(handler_name)
    exp_cache = conf_instances.get("exp_cache", None)
    st.sidebar.title("Filter Experiments")

    exp_manager = exp_manager_factory(id(storage))
    exp_list: List[ExperimentInfo] = query_experiments(storage)
    exps_to_load = select_to_load_exps(exp_list, exp_manager)
    experiments = load_experiments(
        storage,
        exps_to_load,
        local_exp_cache=exp_cache,
        image_loader_factory=conf_instances["image_loader_factory"],
        df_loader_factory=conf_instances["df_loader_factory"],
    )
    for experiment in experiments:
        exp_manager.add_experiment(experiment)
    if exp_manager.get_exp_count() > 0:
        exp_filter_list: List[ExperimentFilter] = conf_instances["sidebar_filters"]
        expdata_list: List[ExperimentData] = exp_manager.get_experiments()
        for exp_filter in exp_filter_list:
            exp_filter.render(expdata_list)
        for exp_filter in exp_filter_list:
            expdata_list = exp_filter.filter(expdata_list)

        exp_id_list: List[str] = [x.exp_info.short_id for x in expdata_list]
        conf_instances["component"].render(exp_manager, storage, exp_id_list)
    else:
        st.markdown("No experiments downloaded!")


def run_dashboard_with_configs_from_path(config_path: str):
    """Runs the dashboard using configs from a given path"""
    config = load_hydra_conf(config_path)
    st.set_page_config(
        layout="wide", page_title=config["title"], page_icon=config.get("icon", None)
    )
    conf_instances = cached_instantiate(config)
    run_dashboard(conf_instances)


if __name__ == "__main__":
    arg_conf_path: str = sys.argv[1]
    GlobalHydra.instance().clear()
    run_dashboard_with_configs_from_path(arg_conf_path)
