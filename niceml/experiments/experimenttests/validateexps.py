from os import listdir
from os.path import join, splitext
from typing import List, Optional

from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem

from niceml.data.storages.fsfilesystemstorage import FsFileSystemStorage
from niceml.data.storages.fsspecstorage import FSSpecStorage
from niceml.experiments.expdatalocalstorageloader import create_expdata_from_local_storage
from niceml.experiments.experimenterrors import EmptyExperimentError
from niceml.experiments.experimenttests.exptests import (
    ExperimentTest,
    ExpTestResult,
    TestStatus,
)
from niceml.utilities.ioutils import list_dir, read_parquet


class ModelsSavedExpTest(ExperimentTest):
    def __init__(self, model_subfolder: str = "models", model_exts: List[str] = None):
        self.model_subfolder = model_subfolder
        self.model_exts = [".pkl", ".hdf5"] if model_exts is None else model_exts

    def __call__(
        self, experiment_path: str, file_system: Optional[AbstractFileSystem] = None
    ) -> ExpTestResult:
        file_system = file_system or LocalFileSystem()
        model_path = join(experiment_path, self.model_subfolder)

        model_files: List[str] = [
            x
            for x in list_dir(model_path, file_system=file_system)
            if splitext(x)[1] in self.model_exts
        ]
        if len(model_files) == 0:
            return ExpTestResult(
                TestStatus.FAILED,
                self.__class__.__name__,
                "The experiment hasn't saved any models!",
            )
        else:
            return ExpTestResult(
                TestStatus.OK,
                self.__class__.__name__,
                f"Models saved: {len(model_files)}",
            )


class ParqFilesNoNoneExpTest(ExperimentTest):
    def __call__(
        self, experiment_path: str, file_system: Optional[AbstractFileSystem] = None
    ) -> ExpTestResult:
        file_system = file_system or LocalFileSystem()
        parq_files: List[str] = [
            x
            for x in list_dir(experiment_path, file_system=file_system)
            if x.endswith(".parq")
        ]
        for parq_name in parq_files:
            cur_fp = join(experiment_path, parq_name)
            cur_df = read_parquet(cur_fp, file_system=file_system)
            if cur_df.isnull().values.any():
                return ExpTestResult(
                    TestStatus.FAILED,
                    self.__class__.__name__,
                    f"Nans are found in {parq_name}",
                )
            else:
                return ExpTestResult(
                    TestStatus.OK, self.__class__.__name__, "No Nans were found!"
                )
        return ExpTestResult(
            TestStatus.OK, self.__class__.__name__, "No parquet files present!"
        )


class ExpEmptyTest(ExperimentTest):
    def __call__(
        self, experiment_path: str, file_system: Optional[AbstractFileSystem] = None
    ) -> ExpTestResult:
        file_system = file_system or LocalFileSystem()
        try:
            storage = FsFileSystemStorage(
                file_system=file_system, root_dir=experiment_path
            )
            create_expdata_from_local_storage("", storage)
        except EmptyExperimentError:
            return ExpTestResult(
                TestStatus.FAILED, self.__class__.__name__, "Experiment is empty!"
            )
        return ExpTestResult(
            TestStatus.OK, self.__class__.__name__, "Experiment files are present."
        )
