"""Module for SimpleImageLoader"""
from os.path import join
from typing import Optional

import numpy as np

from niceml.data.dataloaders.factories.imageloaderfactory import ImageLoaderFactory
from niceml.data.dataloaders.interfaces.imageloader import ImageLoader
from niceml.data.storages.localstorage import LocalStorage
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.loaddatafunctions import LoadImageFile
from niceml.utilities.imagesize import ImageSize


class SimpleImageLoader(ImageLoader):
    """Simple image loader that loads an image"""

    def __init__(
        self,
        storage: Optional[StorageInterface] = None,
        working_dir: Optional[str] = None,
        output_dtype=np.uint8,
    ):
        self.storage = storage or LocalStorage()
        self.output_dtype = output_dtype
        self.working_dir = working_dir

    def __call__(
        self, filepath: str, target_size: Optional[ImageSize] = None
    ) -> np.ndarray:
        target_path = join(self.working_dir, filepath) if self.working_dir else filepath
        return LoadImageFile(target_size, self.output_dtype).load_data(
            target_path, self.storage
        )


class SimpleImageLoaderFactory(
    ImageLoaderFactory
):  # pylint: disable=too-few-public-methods
    """SimpleImageLoaderFactory for image files"""

    def create_image_loader(
        self, storage: StorageInterface, working_dir: str
    ) -> ImageLoader:
        """Creates an instance of ImageLoader"""
        return SimpleImageLoader(storage, working_dir)
