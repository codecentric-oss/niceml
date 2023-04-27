"""Module for MetaVisComponent for the dashboard"""

import contextlib
from typing import List, Optional

import streamlit as st

from niceml.dashboard.components.expviscomponent import ExpVisComponent
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentmanager import ExperimentManager
from niceml.experiments.metainfotables import MetaTable


class MetaVisComponent(ExpVisComponent):
    """Dashboard component to show Meta information about the experiments"""

    def __init__(self, meta_tables: List[MetaTable], **kwargs):
        super().__init__(**kwargs)
        self.meta_tables = meta_tables

    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_ids: List[str],
        subset_name: Optional[str] = None,
    ):
        """renders this component in a streamlit table"""
        exps: List[ExperimentData] = [
            exp_manager.get_exp_by_id(exp_id) for exp_id in exp_ids
        ]
        for meta_table in self.meta_tables:
            with contextlib.suppress(AssertionError, IndexError):
                df_metadata = meta_table(exps)
                st.subheader(meta_table.get_name())
                st.table(df_metadata)
