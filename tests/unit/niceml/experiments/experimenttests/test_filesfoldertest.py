from os import makedirs
from os.path import isdir, isfile, join
from tempfile import TemporaryDirectory
from typing import List

import pytest

from niceml.experiments.experimenttests.checkfilesfolderstest import (
    CheckFilesFoldersTest,
)
from niceml.experiments.experimenttests.exptests import ExpTestResult, TestStatus


@pytest.fixture
def work_dir() -> str:
    with TemporaryDirectory() as tmp_dir:
        t_dir = join(tmp_dir, "test")
        makedirs(t_dir)
        assert isdir(t_dir)
        t_file = join(t_dir, "file.txt")
        open(t_file, "w").close()
        assert isfile(t_file)
        yield tmp_dir


@pytest.mark.parametrize(
    "file_list,folder_list,target",
    [
        ([], None, TestStatus.OK),
        ([join("test", "file.txt")], [], TestStatus.OK),
        (None, ["test"], TestStatus.OK),
        (["false"], [], TestStatus.FAILED),
        ([], ["false"], TestStatus.FAILED),
    ],
)
def test_check_files_folder(
    file_list: List[str], folder_list: List[str], target: TestStatus, work_dir: str
):
    test = CheckFilesFoldersTest(file_list, folder_list)
    pred: ExpTestResult = test(work_dir)
    assert pred.status == target
