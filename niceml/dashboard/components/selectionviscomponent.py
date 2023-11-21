""" module for selection vis component """
from typing import List, Optional, Tuple

from nicegui import ui
from PIL import Image

from niceml.config.subsetnames import get_eval_save_names
from niceml.dashboard.components.expviscomponent import (
    ExpVisComponent,
    SingleExpVisComponent,
)
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentmanager import ExperimentManager


class SelectionVisComponent(ExpVisComponent):
    """A component where you can select one sub component"""

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
        self.container = None

    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_ids: List[str],
        subset_name: Optional[str] = None,
        update: bool = False,
    ):

        """Render function to display component in streamlit"""
        if len(exp_ids) > 0:
            self.get_exp_id_and_subset_name(
                exp_manager,
                storage_interface,
                exp_ids,
                subset_name,
            )

    def full_render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_id: List[str],
        subset_name: Optional[str] = None,
    ):
        self.container.clear()
        with self.container:
            for comp in self.vis_components:
                comp.render(
                    exp_manager,
                    storage_interface,
                    exp_id,
                    subset_name,
                )

    def get_images(self) -> List[Image.Image]:
        """Returns images from sub components"""
        images: List[Image.Image] = []
        for _, vis_comp in self.vis_components:
            images += vis_comp.get_images()
        return images

    def get_exp_id_and_subset_name(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_ids: List[str],
        subset_name: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Gets the exp_id and subset_name from the user via streamlit"""
        if self.use_subset_selection:
            with ui.row().classes("w-full"):
                with ui.column().classes("w-1/2"):
                    # Todo Fix
                    exp_id = ui.select(
                        exp_ids,
                        label="Select ExpID",
                        value=f"selectbox-expid-{self.component_name}",
                        on_change=lambda e: self.full_render(
                            exp_manager=exp_manager,
                            storage_interface=storage_interface,
                            exp_id=e.value,
                            subset_name=subset_name,
                        ),
                    ).classes("w-72")
                with ui.column().classes("w-1/2"):
                    subset_name = ui.select(
                        self.subset_names,
                        label="Select subset",
                        value=f"selectbox-subset" f"-{self.component_name}",
                        on_change=lambda e: self.full_render(
                            exp_manager=exp_manager,
                            storage_interface=storage_interface,
                            exp_id=exp_ids,
                            subset_name=e.value,
                        ),
                    ).classes("w-72")
        else:
            exp_id = ui.select(
                exp_ids,
                label="Select ExpID",
                value=f"selectbox-expid-{self.component_name}",
                on_change=lambda e: self.full_render(
                    exp_manager=exp_manager,
                    storage_interface=storage_interface,
                    exp_id=e.value,
                    subset_name="",
                ),
            ).classes("w-72")
            subset_name = ""
        self.container = ui.column()
        # return exp_id.value, subset_name
