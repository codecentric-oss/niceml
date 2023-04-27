"""Module for ExpVisComponent for the dashboard"""
from abc import ABC, abstractmethod
from typing import Any, List, Optional

import streamlit as st
from PIL import Image

from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentmanager import ExperimentManager
from niceml.experiments.metafunctions import MetaFunction


class RenderingError(Exception):
    """Error when component could not be rendered"""


class ExpVisComponent(ABC):
    """Basic dashboard component to visualize experiments"""

    def __init__(
        self,
        component_name: Optional[str] = None,
        meta_function: Optional[MetaFunction] = None,
        target_value_list: Optional[List[Any]] = None,
        assert_on_error: bool = False,
    ):
        # Create empty list for chart images
        self.component_name: Optional[str] = component_name
        self.chart_images_list: List[Image.Image] = []
        self.meta_function = meta_function
        self.target_value_list = [] if target_value_list is None else target_value_list
        self.assert_on_error = assert_on_error

    def get_component_name(self) -> Optional[str]:
        """Returns the components_name for visualization"""
        return self.component_name

    def render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_ids: List[str],
        subset_name: Optional[str] = None,
    ):
        """Called when a component is rendered"""
        try:
            if self.meta_function is None:
                self._render(exp_manager, storage_interface, exp_ids, subset_name)
            else:
                filtered_exp_list: List[str] = []
                for exp_id in exp_ids:
                    exp_data: ExperimentData = exp_manager.get_exp_by_id(exp_id)
                    meta_target = self.meta_function(exp_data)
                    if meta_target in self.target_value_list:
                        filtered_exp_list.append(exp_id)
                self._render(
                    exp_manager, storage_interface, filtered_exp_list, subset_name
                )
        except Exception as error:  # pylint: disable=broad-except
            st.error(f"Rendering failed: {error}")
            if self.assert_on_error:
                raise error

    @abstractmethod
    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_ids: List[str],
        subset_name: Optional[str] = None,
    ):
        """Used by the render method to render the individual component"""

    def get_images(self) -> List[Image.Image]:
        """Returns the chart images"""
        return self.chart_images_list


class SingleExpVisComponent(ABC):
    """Visualization component for a single experiment"""

    def __init__(
        self,
        meta_function: Optional[MetaFunction] = None,
        target_value_list: Optional[List[Any]] = None,
        assert_on_error: bool = False,
    ):
        # Create empty list for chart images
        self.chart_images_list: List[Image.Image] = []
        self.meta_function = meta_function
        self.target_value_list = [] if target_value_list is None else target_value_list
        self.assert_on_error = assert_on_error

    def render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_id: str,
        subset_name: Optional[str] = None,
    ):
        """Called when a component is rendered"""
        try:
            if self.meta_function is None:
                self._render(exp_manager, storage_interface, exp_id, subset_name)
            else:
                exp_data: ExperimentData = exp_manager.get_exp_by_id(exp_id)
                meta_target = self.meta_function(exp_data)
                if meta_target in self.target_value_list:
                    self._render(exp_manager, storage_interface, exp_id, subset_name)
        except RenderingError as error:
            st.error(f"Rendering failed: {error}")
            if self.assert_on_error:
                raise error

    @abstractmethod
    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_id: str,
        subset_name: Optional[str] = None,
    ):
        """Used by the render method to render the individual component"""

    def get_images(self) -> List[Image.Image]:
        """Returns the chart images"""
        return self.chart_images_list
