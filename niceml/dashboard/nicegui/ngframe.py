from contextlib import contextmanager
from dataclasses import dataclass
from typing import List

from nicegui import ui


@dataclass
class SiteRefs:
    name: str
    target: str


class NgFrameFactory:
    def __init__(
        self,
        title: str,
        site_refs: List[SiteRefs],
    ):
        self.title = title
        self.site_refs = site_refs


    def __call__(self, navtitle: str):
        return ng_frame(self.title,
                        navtitle,
                        self.site_refs)


@contextmanager
def ng_frame(
    title: str,
    navtitle: str,
    site_refs: List[SiteRefs],
):
    """Custom page frame to share the same styling and behavior across all pages"""
    ui.colors(
        primary="#6E93D6", secondary="#53B689", accent="#111B1E", positive="#53B689"
    )
    with ui.header().classes("justify-between text-white"):
        ui.label(title).classes("font-bold")
        ui.label(navtitle)
        with ui.row():
            for site_ref in site_refs:
                ui.link(site_ref.name, site_ref.target).classes(replace="text-white")
    with ui.column().classes("w-full"):
        yield

    with ui.footer().classes("justify-between text-white"):
        ui.label("Denis")