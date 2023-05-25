"""module with prefixviscomponent"""
import logging
from collections import defaultdict
from typing import Dict, List, Optional

from niceml.dashboard.components.expviscomponent import ExpVisComponent
from niceml.dashboard.nicegui.ngtabs import NGTab, NgTabView
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentmanager import ExperimentManager


class TabViewComponent(ExpVisComponent):
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
        self.tab_list = None

    def get_exp_dict(self, exp_ids: List[str], exp_manager: ExperimentManager):
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
        return exp_dict

    def _render(
        self,
        exp_manager: ExperimentManager,
        cloud_storage_interface: StorageInterface,
        exp_ids,
        subset_name: Optional[str] = None,
        update: bool = False,
    ):

        """Render the corresponding prefixes"""
        exp_dict = self.get_exp_dict(exp_ids, exp_manager)
        comp_names: List[str] = []
        for comp_key, cur_comps in self.components.items():
            if comp_key in exp_dict:
                for comp in cur_comps:
                    comp_names.append(comp.get_component_name())
            if not update:
                self.tab_list = NgTabView(
                    [
                        NGTab(
                            comp_name,
                            component,
                        )
                        for (comp_name, component) in zip(comp_names, cur_comps)
                    ],
                    self.components,
                )

                self.tab_list.render(
                    exp_manager, cloud_storage_interface, exp_dict, subset_name, update
                )
            else:
                self.tab_list.render_on_change(
                    exp_manager, cloud_storage_interface, exp_dict, subset_name, update
                )
