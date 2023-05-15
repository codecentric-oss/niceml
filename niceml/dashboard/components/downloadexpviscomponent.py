"""module for download experiments"""
import shutil
from os.path import basename, join
from typing import List, Optional

import streamlit as st

from niceml.dashboard.components.expviscomponent import ExpVisComponent
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentmanager import ExperimentManager
from niceml.storages.abs import get_files_to_download


class DownloadVisu(ExpVisComponent):
    """Visualization of the download dialog"""

    def _render(  # pylint: disable=too-many-locals
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_ids: List[str],
        subset_name: Optional[str] = None,
    ):
        """Generate the visualization for the experiment data download"""
        experiment_id = st.selectbox("Download data of experiment", exp_ids)
        experiment_filepath = exp_manager.get_exp_by_id(experiment_id).dir_name
        download_directory = join("experiment_outputs", basename(experiment_filepath))
        include_models = st.checkbox("Include Models", value=True)
        if st.button("Create zip file"):
            self._download_experiment_files(
                storage_interface,
                experiment_filepath,
                download_directory,
                include_models,
            )

    def _download_experiment_files(
        self,
        storage_interface: StorageInterface,
        experiment_filepath: str,
        download_directory: str,
        include_models: bool,
    ):
        """
        Downloads the files of an experiment and creates a zip file of
        them. It also deletes the temporary directory where they were
        downloaded to.

        Args:
            self: Refer to the instance of the class
            storage_interface: Download the files from the blob storage
            experiment_filepath: Get the name of the experiment
            download_directory: Create a directory to download the files
                into
            include_models: Determine whether to include the model files
                in the download
        """
        full_download_dict = get_files_to_download(
            storage_interface,
            experiment_filepath,
            download_directory,
        )
        download_dict = {
            blob_path: blob_target
            for blob_path, blob_target in full_download_dict.items()
            if include_models or not blob_path.endswith(".hdf5")
        }
        download_count = len(download_dict)
        status_text = st.empty()
        prog_bar = st.progress(0)
        for idx, blob_path in enumerate(download_dict):
            status_text.text(f"({idx + 1}/{download_count}) - File: {blob_path}")
            prog_bar.progress((idx + 1) / download_count)
            storage_interface.download_data(blob_path, download_dict[blob_path])
        self.create_download_zip(
            download_directory,
            download_directory,
            filename=f"{basename(experiment_filepath)}.zip",
        )
        shutil.rmtree(download_directory)

    @staticmethod
    def create_download_zip(zip_directory: str, zip_path: str, filename: str):
        """
        Zip a directory and provide a download link to the zipped
        file within a streamlit application

        Args:
            zip_directory: Path of the directory that should be zipped
            zip_path: Path of the directory that should contain the
                output zip file
            filename: Name of the generated zip file
        """
        shutil.make_archive(zip_path, "zip", zip_directory)
        with open(f"{zip_path}.zip", "rb") as file:
            st.download_button(
                label="Download ZIP",
                data=file,
                file_name=filename,
                mime="application/zip",
            )
