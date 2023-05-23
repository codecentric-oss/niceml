"""module for LinearVisComponent"""
from typing import List, Optional

from PIL import Image

from niceml.dashboard.components.expviscomponent import ExpVisComponent
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentmanager import ExperimentManager


class LinearVisComponent(ExpVisComponent):
    """Visualizes ExpVisComponents one after another"""

    def __init__(
        self,
        component_name: str,
        vis_components: List[ExpVisComponent],
        **kwargs,
    ):
        super().__init__(component_name=component_name, **kwargs)
        self.component_name = component_name
        self.vis_components: List[ExpVisComponent] = vis_components

    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_ids: List[str],
        subset_name: Optional[str] = None,
        update: bool = False,
    ):
        if len(exp_ids) > 0:
            for comp in self.vis_components:
                comp.render(
                    exp_manager, storage_interface, exp_ids, subset_name, update
                )

    def get_images(self) -> List[Image.Image]:
        """gets all images from the subcomponents and returns them"""
        images: List[Image.Image] = []
        for vis_comp in self.vis_components:
            images += vis_comp.get_images()
        return images
