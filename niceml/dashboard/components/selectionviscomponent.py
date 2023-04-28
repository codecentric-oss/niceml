"""Module for SelectionVisComponent for the dashboard"""
from typing import List, Optional, Tuple

import streamlit as st
from PIL import Image

from niceml.config.subsetnames import get_eval_save_names
from niceml.dashboard.components.expviscomponent import (
    ExpVisComponent,
    SingleExpVisComponent,
)
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentmanager import ExperimentManager


class SelectionVisComponent(ExpVisComponent):
    """Dashboard component where one can select one subcomponent to visualize"""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        component_name: str,
        vis_components: List[SingleExpVisComponent],
        expanded: bool = False,
        subset_names: Optional[List[str]] = None,
        use_subset_selection: bool = True,
        **kwargs,
    ):
        super().__init__(component_name=component_name, **kwargs)
        self.vis_components: List[SingleExpVisComponent] = vis_components
        self.expanded = expanded
        self.subset_names = subset_names or get_eval_save_names()
        self.use_subset_selection = use_subset_selection

    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_ids: List[str],
        subset_name: Optional[str] = None,
    ):
        """Render function to display component on dashboard"""
        if len(exp_ids) > 0:
            exp_id, subset_name = self.get_exp_id_and_subset_name(exp_ids)
            for comp in self.vis_components:
                comp.render(
                    exp_manager,
                    storage_interface,
                    exp_id,
                    subset_name,
                )

    def get_images(self) -> List[Image.Image]:
        """Returns images from subcomponents"""
        images: List[Image.Image] = []
        for _, vis_comp in self.vis_components:
            images += vis_comp.get_images()
        return images

    def get_exp_id_and_subset_name(self, exp_ids: List[str]) -> Tuple[str, str]:
        """Gets the experiment id and subset name from the user selection via streamlit"""
        if self.use_subset_selection:
            col1, col2 = st.columns(2)
            exp_id = col1.selectbox(
                "Select ExpID",
                options=exp_ids,
                key=f"selectbox-expid-{self.component_name}",
            )
            subset_name = col2.selectbox(
                "Select subset",
                options=self.subset_names,
                key=f"selectbox-subset" f"-{self.component_name}",
            )
        else:
            exp_id = st.selectbox(
                "Select ExpID",
                options=exp_ids,
                key=f"selectbox-expid-{self.component_name}",
            )
            subset_name = ""

        return exp_id, subset_name
