"""Module for config visu component"""

from typing import Optional

import yaml
from nicegui import ui

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
        update: bool = False,
    ):
        """
        Rendering a selectbox to select a configuration file of the experiment and display its
        contents as a yaml-formatted code block.

        Args:
            exp_manager: Experiment manager to get the data of the selected experiment
            storage_interface: Storage Interface to access the data of the selected experiment
            exp_id: Current selected experiment
            subset_name: Name of the dataset

        """
        self.exp: ExperimentData = exp_manager.get_exp_by_id(exp_id)

        sel_conf = ui.select(
            sorted(self.exp.exp_dict_data.keys()),
            label="Config file",
            on_change=lambda e: self.update_config(e.value),
        ).classes("w-96")
        self.container = ui.column()

    def update_config(self, configs):
        self.container.clear()
        with self.container:
            ui.markdown(
                f"<pre><code>"
                f"{yaml.dump(self.exp.exp_dict_data[configs])}"
                f"</code></pre>"
            )
