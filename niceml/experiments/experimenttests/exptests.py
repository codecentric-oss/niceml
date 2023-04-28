"""Module for exptests"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from fsspec import AbstractFileSystem


class TestStatus(str, Enum):
    OK = "OK"
    FAILED = "FAILED"


@dataclass
class ExpTestResult(object):
    """Result of an experiment test"""

    status: TestStatus
    name: str
    message: str

    def to_dict(self) -> dict:
        return dict(status=self.status.name, name=self.name, message=self.message)

    def __str__(self):
        return f"{self.status} - {self.name} - {self.message}"


class ExperimentTest(ABC):
    """Abstract class for an experiment test"""

    def get_test_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def __call__(
        self, experiment_path: str, file_system: Optional[AbstractFileSystem] = None
    ) -> ExpTestResult:
        pass
