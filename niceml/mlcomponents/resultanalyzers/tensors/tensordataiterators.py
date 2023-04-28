"""Module for tensordataiterator"""
from abc import ABC, abstractmethod
from typing import Optional

from fsspec import AbstractFileSystem


class TensordataIterator(ABC):
    """TensordataIterators are used in the tensoranalyser
    to load and iterate over the data."""

    @abstractmethod
    def open(self, path: str, file_system: Optional[AbstractFileSystem] = None):
        """Method to start with before using the iterator"""

    @abstractmethod
    def __iter__(self):
        """Returning an iterator"""

    @abstractmethod
    def __getitem__(self, item):
        """Access to an specific item"""
