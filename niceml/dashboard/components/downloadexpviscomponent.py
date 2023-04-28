"""Module for the visu component that downloads an experiment"""
from typing import List, Optional

from niceml.dashboard.components.expviscomponent import ExpVisComponent
from niceml.dashboard.remotettrainutils import download_visu
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentdownloader import ExperimentDownloader
from niceml.experiments.experimentmanager import ExperimentManager


class DownloadExpVisComponent(ExpVisComponent):
    """
    Dashboard component to download the selected experiment
    """

    def __init__(self, local_storage_path: str = "experiments", **kwargs):
        super().__init__(**kwargs)
        self.local_storage_path = local_storage_path

    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_ids: List[str],
        subset_name: Optional[str] = None,
    ):
        sel_exp_data: List[ExperimentData] = [
            exp_manager.get_exp_by_id(cur_id) for cur_id in exp_ids
        ]

        exp_downloader = ExperimentDownloader(
            sel_exp_data, storage_interface, self.local_storage_path, ""
        )
        download_visu(exp_downloader)
