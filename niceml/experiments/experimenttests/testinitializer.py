"""Module for testinitializer"""
import logging
from os.path import join
from typing import List, Optional

import pandas as pd
from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem

from niceml.experiments.experimenttests.exptests import (
    ExperimentTest,
    ExpTestResult,
    TestStatus,
)
from niceml.utilities.ioutils import write_csv


class ExperimentTestFailedError(Exception):
    """Exception for when an experiment test fails"""


class ExpTestProcess(object):  # pylint: disable=too-few-public-methods
    """Class to execute a list of ExperimentTests"""

    def __init__(
        self,
        test_list: List[ExperimentTest],
        csv_out_name: str = "exp_tests.csv",
        raise_exception: bool = True,
        store_results: bool = True,
    ):
        self.test_list = test_list
        self.csv_out_name = csv_out_name
        self.raise_exception = raise_exception
        self.store_results = store_results

    def __call__(
        self,
        input_folder: str,
        output_folder: Optional[str] = None,
        file_system: Optional[AbstractFileSystem] = None,
    ):
        """Execute the list of tests and return a list of ExpTestResults"""
        file_system = file_system or LocalFileSystem()
        if output_folder is None:
            output_folder = input_folder
        test_result_list: List[ExpTestResult] = []
        failed: List[ExpTestResult] = []
        for test_obj in self.test_list:
            test_result = test_obj(input_folder, file_system)
            if test_result.status == TestStatus.FAILED:
                failed.append(test_result)
            test_result_list.append(test_result)

        out_path = join(output_folder, self.csv_out_name)
        if self.store_results:
            dataframe: pd.DataFrame = pd.DataFrame(
                [x.to_dict() for x in test_result_list]
            )
            write_csv(
                dataframe, out_path, file_system=file_system, sep=";", decimal=","
            )

        if len(failed) > 0 and self.raise_exception:
            for failed_exp in failed:
                logging.getLogger(__name__).error(str(failed_exp))
            raise ExperimentTestFailedError(
                f"Experiment Tests Failed: {failed} Info at: {out_path}"
            )
