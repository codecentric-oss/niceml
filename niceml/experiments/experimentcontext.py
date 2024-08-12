"""Module for the ExperimentContext"""
import logging
from dataclasses import dataclass
from os.path import join
from typing import Optional, Union, Literal

import pandas as pd
from altair import Chart
from fsspec import AbstractFileSystem
from PIL import Image

from niceml.config.envconfig import LAST_MODIFIED_KEY
from niceml.config.hydra import instantiate_from_yaml
from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.experiments.expfilenames import ExperimentFilenames, OpNames
from niceml.utilities.fsspec.locationutils import LocationConfig, open_location
from niceml.utilities.ioutils import (
    read_csv,
    read_image,
    read_parquet,
    read_yaml,
    write_csv,
    write_image,
    write_parquet,
    write_yaml,
    write_json,
    read_json,
    write_chart,
)
from niceml.utilities.timeutils import generate_timestamp


@dataclass
class ExperimentContext:
    """ExperimentContext to provide the ids and storage"""

    fs_config: Union[LocationConfig, dict]
    run_id: str
    short_id: str

    def write_parquet(
        self,
        dataframe: pd.DataFrame,
        data_path: str,
        compression: Optional[str] = "gzip",
        apply_last_modified: bool = True,
        **kwargs,
    ):
        """
        Writes the dataframe as parquet file relative to the experiment.

        Args:
            dataframe: data to save as parquet file
            data_path: path to save the data to (relative to experiment folder)
            compression: optional compression argument (defaults to "gzip")
            apply_last_modified: Whether to update the last modified timestamp
                saved in the experiment info to track a change in the experiment
            **kwargs: additional keywords for save function
        """
        with open_location(self.fs_config) as (file_system, root_path):
            write_parquet(
                dataframe,
                # TODO: change with join_fs_path
                join(root_path, data_path),
                compression=compression,
                file_system=file_system,
                **kwargs,
            )
        if apply_last_modified:
            self.update_last_modified()

    def read_parquet(self, data_path: str) -> pd.DataFrame:
        """
        Reads the dataframe as parquet file relative to the experiment.

        Args:
            data_path: path to the parquet file to read (relative to experiment folder)

        Returns:
            DataFrame containing the data of the parquet file
        """
        with open_location(self.fs_config) as (file_system, root_path):
            return read_parquet(join(root_path, data_path), file_system=file_system)

    def read_yaml(self, data_path: str) -> dict:
        """
        Reads the yaml file relative to the experiment.

        Args:
            data_path: path to the yaml file to read (relative to experiment folder)

        Returns:
            Dictionary containing the data of the yaml file
        """
        with open_location(self.fs_config) as (file_system, root_path):
            return read_yaml(join(root_path, data_path), file_system=file_system)

    def write_yaml(
        self, data: dict, data_path: str, apply_last_modified: bool = True, **kwargs
    ):
        """
        Writes the yaml file relative to the experiment.

        Args:
            data: dictionary of data to be written to the yaml file
            data_path: path to save the data to (relative to experiment folder)
            apply_last_modified: Whether to update the last modified timestamp
                saved in the experiment info to track a change in the experiment
            **kwargs: additional keywords for save function
        """
        with open_location(self.fs_config) as (file_system, root_path):
            write_yaml(
                data,
                join(root_path, data_path),
                file_system=file_system,
                **kwargs,
            )
        if apply_last_modified:
            self.update_last_modified()

    def read_csv(self, data_path: str) -> pd.DataFrame:
        """
        Reads a csv file relative to the experiment.

        Args:
            data_path: path to the csv file to read (relative to experiment folder)

        Returns:
            DataFrame containing the data of the csv file
        """
        with open_location(self.fs_config) as (file_system, root_path):
            return read_csv(join(root_path, data_path), file_system=file_system)

    def write_csv(
        self,
        data: pd.DataFrame,
        data_path: str,
        apply_last_modified: bool = True,
        **kwargs,
    ):
        """
        Writes a csv file relative to the experiment.

        Args:
            data: Dataframe to save as csv file
            data_path: path to save the data to (relative to experiment folder)
            apply_last_modified: Whether to update the last modified timestamp
                saved in the experiment info to track a change in the experiment
            **kwargs: additional keywords for save function
        """
        with open_location(self.fs_config) as (file_system, root_path):
            write_csv(
                data,
                join(root_path, data_path),
                file_system=file_system,
                **kwargs,
            )
        if apply_last_modified:
            self.update_last_modified()

    def write_json(
        self,
        data: dict,
        data_path: str,
        apply_last_modified: bool = True,
        **kwargs,
    ):
        """
        Writes a json file relative to the experiment.

        Args:
            data: dictionary to write to json file
            data_path: path to save the json file to (relative to experiment folder)
            apply_last_modified: Whether to update the last modified timestamp
                saved in the experiment info to track a change in the experiment
            **kwargs: additional keywords for save function
        """
        with open_location(self.fs_config) as (file_system, root_path):
            write_json(
                data,
                join(root_path, data_path),
                file_system=file_system,
                **kwargs,
            )
        if apply_last_modified:
            self.update_last_modified()

    def read_json(self, data_path: str) -> dict:
        """
        Reads the json file relative to the experiment.

        Args:
            data_path: path to the json file to read (relative to experiment folder)

        Returns:
            the json file contents as a dictionary
        """
        with open_location(self.fs_config) as (file_system, root_path):
            return read_json(join(root_path, data_path), file_system=file_system)

    def write_image(
        self,
        image: Image.Image,
        data_path: str,
        apply_last_modified: bool = True,
        **kwargs,
    ):
        """
        Writes an image relative to the experiment

        Args:
            image: pillow image to save
            data_path: path to save the image to (relative to experiment folder)
            apply_last_modified: Whether to update the last modified timestamp
                of the experiment
            **kwargs: additional keywords for save function
        """
        with open_location(self.fs_config) as (file_system, root_path):
            write_image(
                image,
                join(root_path, data_path),
                file_system=file_system,
                **kwargs,
            )
        if apply_last_modified:
            self.update_last_modified()

    def read_image(self, data_path: str) -> Image.Image:
        """
        Reads an image relative to the experiment

        Args:
            data_path: path to load the image from (inside the experiment folder)

        Returns:
            Image from given file
        """
        with open_location(self.fs_config) as (file_system, root_path):
            return read_image(join(root_path, data_path), file_system=file_system)

    def write_chart(
        self,
        chart: Chart,
        data_path: str,
        apply_last_modified: bool = True,
        file_format: Optional[Literal["json", "html", "png", "svg", "pdf"]] = "html",
        **kwargs,
    ):
        """
        Writes an altair.Chart in given file_format relative to the experiment.

        Args:
            chart: altair chart to save
            data_path: path to save the chart to (inside the experiment folder)
            apply_last_modified: Whether to update the last modified timestamp
                saved in the experiment info to track a change in the experiment
            file_format: file format to save the chart in (json, html, png, svg or pdf)
            **kwargs: additional keywords for save function
        """
        with open_location(self.fs_config) as (file_system, root_path):
            write_chart(
                chart,
                join(root_path, data_path),
                file_system,
                file_format,
                **kwargs,
            )
        if apply_last_modified:
            self.update_last_modified()

    def create_folder(self, folder: str):
        """
        Creates a folder relative to the experiment.

        Args:
            folder: name of folder to create inside the experiment folder
        """
        file_system: AbstractFileSystem
        with open_location(self.fs_config) as (file_system, root_path):
            abs_folder = join(root_path, folder)
            file_system.makedirs(abs_folder, exist_ok=True)

    def instantiate_datadescription_from_yaml(self) -> DataDescription:
        """
        Instantiates a DataDescription from a yaml file. Path to
        yaml file is accessed via the experiment context and must not
        be given.

        Returns:
            DataDescription instance of experiment
        """
        with open_location(self.fs_config) as (exp_fs, exp_root):
            data_description: DataDescription = instantiate_from_yaml(
                join(
                    exp_root,
                    ExperimentFilenames.CONFIGS_FOLDER,
                    OpNames.OP_TRAIN.value,
                    ExperimentFilenames.DATA_DESCRIPTION,
                ),
                file_system=exp_fs,
            )
        return data_description

    def update_last_modified(self, timestamp: Optional[str] = None):
        """
        Updates the last modified timestamp of the experiment info file
        of the experiment. The timestamp is used to track when the
        experiment was changed.

        Args:
            timestamp: new timestamp to save in experiment info

        Raises:
            FileNotFoundError if experiment info file does not exist
        """
        timestamp = timestamp or generate_timestamp()
        try:
            exp_info_dict = self.read_yaml(ExperimentFilenames.EXP_INFO)
            exp_info_dict[LAST_MODIFIED_KEY] = timestamp
            self.write_yaml(
                exp_info_dict, ExperimentFilenames.EXP_INFO, apply_last_modified=False
            )
        except FileNotFoundError:
            logging.getLogger(__name__).warning(
                "Could not update last modified timestamp, because the "
                "experiment info file was not found."
            )
