"""Module for ImageLoaderFactory"""
from abc import ABC, abstractmethod

from niceml.data.dataloaders.interfaces.imageloader import ImageLoader
from niceml.data.storages.storageinterface import StorageInterface


class ImageLoaderFactory(ABC):  # pylint: disable=too-few-public-methods
    """Abstract implementation of ImageLoaderFactory"""

    @abstractmethod
    def create_image_loader(
        self, storage: StorageInterface, working_dir: str
    ) -> ImageLoader:
        """Creates an ImageLoader"""
