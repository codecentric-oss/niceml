""" Module for CheckFilesFoldersTest """
from os.path import isdir, isfile, join
from typing import List, Optional

from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem

from niceml.experiments.experimenttests.exptests import (
    ExperimentTest,
    ExpTestResult,
    TestStatus,
)


class CheckFilesFoldersTest(ExperimentTest):
    def __init__(
        self, files: Optional[List[str]] = None, folders: Optional[List[str]] = None
    ):
        """
        ExperimentTest if files and folders are located in the experiment
        Parameters
        ----------
        files: Optional[List[str]], default None
            All required files with relative path to experiment root
        folders: Optional[List[str]], default None
            All required folders with relative path to experiment root
        """
        self.files = [] if files is None else files
        self.folders = [] if folders is None else folders

    def __call__(
        self, experiment_path: str, file_system: Optional[AbstractFileSystem] = None
    ) -> ExpTestResult:
        file_system = file_system or LocalFileSystem()
        missing_paths: List[str] = []
        for f in self.files:
            if not file_system.isfile(join(experiment_path, f)):
                missing_paths.append(f)

        for f in self.folders:
            if not file_system.isdir(join(experiment_path, f)):
                missing_paths.append(f)

        message = (
            "All files/folder are present!"
            if len(missing_paths) == 0
            else f"Missing files and folders: {missing_paths}"
        )
        status = TestStatus.OK if len(missing_paths) == 0 else TestStatus.FAILED
        return ExpTestResult(status, self.__class__.__name__, message)
