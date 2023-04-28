"""Module for the ExperimentContext"""
from dataclasses import dataclass
from os.path import join
from typing import Optional, Union

import pandas as pd
from fsspec import AbstractFileSystem
from PIL import Image

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
)


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
        **kwargs,
    ):
        """writes the dataframe as parquet file relative to the experiment"""
        with open_location(self.fs_config) as (file_system, root_path):
            write_parquet(
                dataframe,
                # TODO: change with join_fs_path
                join(root_path, data_path),
                compression=compression,
                file_system=file_system,
                **kwargs,
            )

    def read_parquet(self, data_path: str) -> pd.DataFrame:
        """reads the dataframe as parquet file relative to the experiment"""
        with open_location(self.fs_config) as (file_system, root_path):
            return read_parquet(join(root_path, data_path), file_system=file_system)

    def read_yaml(self, data_path: str) -> dict:
        """reads the yaml file relative to the experiment"""
        with open_location(self.fs_config) as (file_system, root_path):
            return read_yaml(join(root_path, data_path), file_system=file_system)

    def write_yaml(self, data: dict, data_path: str, **kwargs):
        """writes the yaml file relative to the experiment"""
        with open_location(self.fs_config) as (file_system, root_path):
            write_yaml(
                data,
                join(root_path, data_path),
                file_system=file_system,
                **kwargs,
            )

    def read_csv(self, data_path: str) -> pd.DataFrame:
        """Reads a csv file relative to the experiment"""
        with open_location(self.fs_config) as (file_system, root_path):
            return read_csv(join(root_path, data_path), file_system=file_system)

    def write_csv(self, data: pd.DataFrame, data_path: str, **kwargs):
        """Writes a csv file relative to the experiment"""
        with open_location(self.fs_config) as (file_system, root_path):
            write_csv(
                data,
                join(root_path, data_path),
                file_system=file_system,
                **kwargs,
            )

    def write_image(self, image: Image.Image, data_path: str):
        """Writes an image relative to the experiment"""
        with open_location(self.fs_config) as (file_system, root_path):
            write_image(image, join(root_path, data_path), file_system=file_system)

    def read_image(self, data_path: str) -> Image.Image:
        """Reads an image relative to the experiment"""
        with open_location(self.fs_config) as (file_system, root_path):
            return read_image(join(root_path, data_path), file_system=file_system)

    def create_folder(self, folder: str):
        """Creates a folder relative to the experiment"""
        file_system: AbstractFileSystem
        with open_location(self.fs_config) as (file_system, root_path):
            abs_folder = join(root_path, folder)
            file_system.makedirs(abs_folder, exist_ok=True)

    def instantiate_datadescription_from_yaml(self) -> DataDescription:
        """Instantiates a DataDescription from a yaml file"""
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
