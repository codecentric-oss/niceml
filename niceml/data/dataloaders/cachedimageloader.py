"""Module for RemoteCachedImageLoader"""
import io
from os import makedirs
from os.path import dirname, isfile, join
from typing import Optional

import numpy as np
from PIL import Image

from niceml.data.dataloaders.factories.imageloaderfactory import ImageLoaderFactory
from niceml.data.dataloaders.interfaces.imageloader import ImageLoader
from niceml.data.storages.storageinterface import StorageInterface
from niceml.utilities.imagesize import ImageSize


class RemoteDiskCacheImageLoader(ImageLoader):
    """Loads and caches remote images on the disk"""

    def __init__(
        self,
        storage: StorageInterface,
        cache_dir: str = "./image_cache",
        working_dir: Optional[str] = None,
        output_dtype=np.uint8,
    ):
        self.storage = storage
        self.working_dir = working_dir
        self.cache_dir = cache_dir
        self.output_dtype = output_dtype

    def __call__(
        self, filepath: str, target_size: Optional[ImageSize] = None
    ) -> np.ndarray:
        target_path = (
            self.storage.join_paths(self.working_dir, filepath)
            if self.working_dir
            else filepath
        )
        cached_filepath: str = join(self.cache_dir, target_path)
        image: Image.Image
        if isfile(cached_filepath):
            image = Image.open(cached_filepath)
        else:
            data = self.storage.download_as_str(target_path)
            image = Image.open(io.BytesIO(data))
            cached_dir = dirname(cached_filepath)
            makedirs(cached_dir, exist_ok=True)
            image.save(cached_filepath)
        if target_size is not None:
            image = image.resize(target_size.to_pil_size())
        return np.array(image, dtype=self.output_dtype)


class RemoteDiskCacheImageLoaderFactory(
    ImageLoaderFactory
):  # pylint: disable=too-few-public-methods
    """Creates RemoteDiskCacheImageLoader"""

    def __init__(self, cache_dir: str = "./image_cache"):
        self.cache_dir = cache_dir

    def create_image_loader(
        self, storage: StorageInterface, working_dir: str
    ) -> ImageLoader:
        """Creates RemoteDiskCacheImageLoader"""
        return RemoteDiskCacheImageLoader(storage, self.cache_dir)
