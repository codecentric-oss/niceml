"""Module for  prefixviscomponent"""
import logging
from collections import defaultdict
from typing import Dict, List, Optional

import streamlit as st

from niceml.dashboard.components.expviscomponent import ExpVisComponent
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentmanager import ExperimentManager


class PrefixVisComponent(ExpVisComponent):
    """This ExpVisComponent allows a rendering regarding the ExperimentPrefixes"""

    def __init__(
        self,
        components: Dict[str, List[ExpVisComponent]],
        use_tabs: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.components = components
        self.use_tabs = use_tabs

    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_ids: List[str],
        subset_name: Optional[str] = None,
    ):
        """
        Takes in an ExperimentManager, a StorageInterface, and a list of experiment ids.
        The _render function then calls the get_exp_prefix() method on each experiment id
        to determine which component it belongs to. If there is no prefix match for that particular
        experiment id, then it will check if "_all_" exists as a key in self.components
        (which means that all experiment types should be rendered).
        If neither of these conditions are met, then we log an error message saying that
        this particular exp cannot be rendered due to its prefix not being found.

        Args:
            exp_manager: ExperimentManager: ExperimentManager to get the experiment data
            storage_interface: StorageInterface: Access the storage
            exp_ids: List[str]: Pass the list of experiment ids to be rendered
            subset_name: Optional[str]: Render the experiment data to a subset

        """
        exp_data_list: List[ExperimentData] = [
            exp_manager.get_exp_by_id(exp_id) for exp_id in exp_ids
        ]
        exp_dict: Dict[str, List[str]] = defaultdict(list)
        for exp_data in exp_data_list:
            prefix = exp_data.get_exp_prefix()
            if prefix in self.components:
                exp_dict[prefix].append(exp_data.get_short_id())
            elif "_all_" in self.components:
                exp_dict["_all_"].append(exp_data.get_short_id())
            else:
                logging.getLogger(  # pylint: disable=logging-fstring-interpolation
                    __name__
                ).warning(
                    f"Exp with id {exp_data.get_short_id()} "
                    f"is not rendered due to prefix: {prefix}"
                )
        comp_index: int = 0
        comp_names: List[str] = []
        for comp_key, cur_comps in self.components.items():
            if comp_key in exp_dict:
                for comp in cur_comps:
                    comp_index += 1
                    comp_names.append(
                        comp.get_component_name() or f"Component {comp_index}"
                    )

        comp_index = 0
        if self.use_tabs:
            st_comp_list = list(st.tabs(comp_names))
        else:
            st_comp_list = [st.expander(label) for label in comp_names]
        for comp_key, cur_comps in self.components.items():
            if comp_key in exp_dict:
                for comp in cur_comps:
                    with st_comp_list[comp_index]:
                        comp.render(
                            exp_manager,
                            storage_interface,
                            exp_dict[comp_key],
                            subset_name,
                        )
                    comp_index += 1
