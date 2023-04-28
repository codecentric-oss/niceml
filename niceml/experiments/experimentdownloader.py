"""module of experiment downloader"""
from os.path import join, relpath, splitext
from typing import List, Set

from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData


# pylint: disable = too-few-public-methods
class Download:
    """Download class for the dashboard"""

    def __init__(
        self, source_file: str, target_file: str, storage_interface: StorageInterface
    ):
        self.source_file = source_file
        self.target_file = target_file
        self.storage_interface = storage_interface

    def __call__(self):
        self.storage_interface.download_data(self.source_file, self.target_file)


class ExperimentDownloader:
    """Class to download experiment data"""

    def __init__(
        self,
        experiments: List[ExperimentData],
        storage_interface: StorageInterface,
        local_store_path: str,
        remote_exp_path: str,
    ):
        self.experiments = experiments
        self.storage_interface = storage_interface
        self.local_store_path = local_store_path
        self.remote_exp_path = remote_exp_path

    def get_all_extensions(self) -> List[str]:
        ext_set: Set[str] = set()
        for cur_exp in self.experiments:
            if cur_exp.all_exp_files is not None:
                for cur_file in cur_exp.all_exp_files:
                    ext_set.add(splitext(cur_file)[1])
        return list(ext_set)

    def get_downloads(self, extension_list: List[str]) -> List[Download]:
        download_list: List[Download] = []
        for cur_exp in self.experiments:
            if cur_exp.all_exp_files is not None:
                for cur_file in cur_exp.all_exp_files:
                    if splitext(cur_file)[1] in extension_list:
                        download_list.append(cur_file)
        download_list = [
            Download(
                x,
                join(self.local_store_path, relpath(x, self.remote_exp_path)),
                self.storage_interface,
            )
            for x in download_list
        ]
        return download_list
