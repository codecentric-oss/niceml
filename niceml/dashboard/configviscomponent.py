"""Module for config visu component"""

from typing import Optional

import streamlit as st
import yaml

from niceml.dashboard.components.expviscomponent import SingleExpVisComponent
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentmanager import ExperimentManager


class ConfigVisComponent(SingleExpVisComponent):
    """Visu component to show the configs of a single experiment as yaml code"""

    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_id: str,
        subset_name: Optional[str] = None,
    ):
        """
        Rendering a select box to select a configuration file of the experiment and display its
        contents as a yaml-formatted code block.

        Args:
            exp_manager: Experiment manager to get the data of the selected experiment
            storage_interface: Storage Interface to access the data of the selected experiment
            exp_id: Current selected experiment
            subset_name: Name of the dataset

        """
        exp: ExperimentData = exp_manager.get_exp_by_id(exp_id)
        config_data = exp.get_config_dict()
        sel_conf = st.selectbox("Config file", options=sorted(config_data.keys()))
        yaml_code = yaml.dump(config_data[sel_conf])
        st.code(yaml_code, language="yaml")
