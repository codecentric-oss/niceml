"""Module for AVC ModelLoader"""
from abc import ABC, abstractmethod
from typing import Any, Optional

from fsspec import AbstractFileSystem


class ModelLoader(ABC):  # pylint: disable=too-few-public-methods
    """Callable that loads models"""

    @abstractmethod
    def __call__(
        self,
        model_path: str,
        file_system: Optional[AbstractFileSystem] = None,
    ) -> Any:
        """Loads the model at the given path"""
