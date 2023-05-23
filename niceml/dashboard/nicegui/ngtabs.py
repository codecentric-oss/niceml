from abc import ABC, abstractmethod
from typing import List

from nicegui import ui



class NGTab:

    # Each Tab gets a function assigned, which can be a single component (Optional: When multiple components, this will be a function that calls
    # all functions for all components).
    def __init__(
        self,
        name: str,
        component,
    ):
        self.name = name
        self.component = component
        self.container = None

    # Function that renders the content of the tab that we is pressed
    def render(
        self, exp_manager, cloud_storage_interface, exp_dict, subset_name, update
    ):
        if self.container is None:
            self.container = ui.column().classes("w-full")
        self.render_on_change(
            exp_manager, cloud_storage_interface, exp_dict, subset_name, update
        )

    def render_on_change(
        self, exp_manager, cloud_storage_interface, exp_dict, subset_name, update
    ):
        self.container.clear()
        with self.container:
            self.component.render(
                exp_manager, cloud_storage_interface, exp_dict, subset_name, update
            )


class NgTabView:
    def __init__(self, tabs: List[NGTab], components):
        self.tabs = tabs
        self.tab_elements = None
        self.panels = None
        self.components = components

    def handle_change(self, msg: dict) -> None:
        name = msg["args"]
        self.tab_elements.props(f"model-value={name}")
        self.panels.props(f"model-value={name}")

    def render(
        self, exp_manager, cloud_storage_interface, exp_dict, subset_name, update
    ):
        self.tab_elements = ui.element("q-tabs").classes("w-full")
        self.panels = ui.element("q-tab-panels").classes("w-full")
        with self.tab_elements.on("update:model-value", self.handle_change):
            [
                ui.element("q-tab")
                .props(f"name={cur_tab.name} label={cur_tab.name}")
                .props("aria-selected=True")
                for cur_tab in self.tabs
            ]

        with self.panels.props("model-value=A animated w-100"):
            for comp_key, _ in self.components.items():
                for cur_tab in self.tabs:
                    with ui.element("q-tab-panel").props(f"name={cur_tab.name}"):
                        cur_tab.render(
                            exp_manager,
                            cloud_storage_interface,
                            exp_dict[comp_key],
                            subset_name,
                            update,
                        )

    def render_on_change(
        self, exp_manager, cloud_storage_interface, exp_dict, subset_name, update
    ):
        # with self.panels.props("model-value=A animated w-100"):
        for cur_tab in self.tabs:
            for comp_key, _ in self.components.items():
                cur_tab.render_on_change(
                    exp_manager,
                    cloud_storage_interface,
                    exp_dict[comp_key],
                    subset_name,
                    update,
                )
