"""module for metaviscomponent"""
import json
from functools import partial
from typing import List, Optional

import pandas as pd
from nicegui import ui

from niceml.dashboard.components.expviscomponent import ExpVisComponent
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentmanager import ExperimentManager
from niceml.experiments.metainfotables import MetaTable


class MetaVisComponent(ExpVisComponent):
    """ExpVisComponent to show meta information about the experiments"""

    def __init__(self, meta_tables: List[MetaTable], **kwargs):
        super().__init__(**kwargs)
        self.meta_tables = meta_tables
        self.grid = None

    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_ids: List[str],
        subset_name: Optional[str] = None,
        update: bool = False,
    ):

        """renders this component in a nicegui table"""
        exps: List[ExperimentData] = [
            exp_manager.get_exp_by_id(exp_id) for exp_id in exp_ids
        ]

        self.grid = {}
        for meta_table in self.meta_tables:
            try:
                df_metadata = meta_table(exps)
                ui.label(meta_table.get_name())
                df_metadata = df_metadata.fillna('N/A')

                self.grid[meta_table.get_name()] = ui.aggrid.from_pandas(df_metadata)

                #self.grid[meta_table.get_name()].call_api_method("sizeColumnsToFit")
                self.grid[meta_table.get_name()].update()


                formatcolumns = FormatColumns(self.grid[meta_table.get_name()])
                with ui.row():
                    ui.button("autocolumnsize", on_click=formatcolumns.format_columns)
                    #ui.button("resetSize", on_click=formatcolumns.autosize)
            except (AssertionError, IndexError):
                pass

class FormatColumns:
    def __init__(self,
                 grid):
        self.grid = grid

    async def format_columns(self) -> None:
        await ui.run_javascript(f"""
            getElement({self.grid.id}).gridOptions.columnApi.autoSizeAllColumns();
        """, respond=False,
        )

    async def autosize(self) -> None:
        await ui.run_javascript(f"""
            console.log(getElement({self.grid.id}).gridOptions.api);
        """, respond=False,
        )
