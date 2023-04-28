"""Module for LoadDataFunctions"""
import io
from abc import ABC, abstractmethod
from typing import Any

import fastparquet
import numpy as np
import pandas as pd
import yaml
from PIL import Image

from niceml.data.storages.storageinterface import StorageInterface
from niceml.utilities.imagesize import ImageSize


class LoadDataFunc(ABC):  # pylint: disable=too-few-public-methods
    """Abstract class to load arbitrary data via a storages"""

    @abstractmethod
    def load_data(self, file_path: str, storage: StorageInterface) -> Any:
        """loads data from cloud storage"""


class LoadYamlFile(LoadDataFunc):  # pylint: disable=too-few-public-methods
    """Loads yaml data from a cloud storage"""

    def load_data(self, file_path: str, storage: StorageInterface):
        data = storage.download_as_str(file_path)
        return yaml.load(data, Loader=yaml.SafeLoader)


class LoadCsvFile(LoadDataFunc):  # pylint: disable=too-few-public-methods
    """Loads csv data from a cloud storage"""

    def load_data(self, file_path: str, storage: StorageInterface):
        data = storage.download_as_str(file_path)
        data_frame = pd.read_csv(io.BytesIO(data))
        return data_frame


class LoadParquetFile(LoadDataFunc):  # pylint: disable=too-few-public-methods
    """Loads parquet data from a cloud storage"""

    def load_data(self, file_path: str, storage: StorageInterface):
        data = storage.download_as_str(file_path)
        if data == b"":
            raise FileNotFoundError("File empty")
        pq_file = io.BytesIO(data)
        data_frame = fastparquet.ParquetFile(pq_file).to_pandas()
        return data_frame


class LoadImageFile(LoadDataFunc):  # pylint: disable=too-few-public-methods
    """Loads image data from a cloud storage"""

    def __init__(self, target_size: ImageSize, output_dtype=np.uint8):
        self.target_size = target_size
        self.output_dtype = output_dtype

    def load_data(self, file_path: str, storage: StorageInterface):
        data = storage.download_as_str(file_path)
        image: Image.Image = Image.open(io.BytesIO(data))
        if self.target_size is not None:
            image = image.resize(self.target_size.to_pil_size())
        img_array = np.array(image, dtype=self.output_dtype)

        return img_array
