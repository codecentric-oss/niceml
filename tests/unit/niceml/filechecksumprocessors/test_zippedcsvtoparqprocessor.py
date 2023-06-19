import shutil
from os.path import join
from tempfile import TemporaryDirectory
from typing import List

import pandas as pd
import pytest

from niceml.filechecksumprocessors.zippedcsvtoparqprocessor import (
    ZippedCsvToParqProcessor,
)
from niceml.utilities.fsspec.locationutils import LocationConfig, open_location
from niceml.utilities.ioutils import write_csv, list_dir, read_parquet, read_yaml


@pytest.fixture(scope="session")
def tmp_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp


@pytest.fixture(scope="session")
def csv_data() -> List[pd.DataFrame]:
    csv_data = []
    for file_count in range(5):
        data = []
        for line_count in range(20):
            data.append({"id": line_count, "name": f"name{line_count}"})
        df = pd.DataFrame(data)
        csv_data.append(df)
    return csv_data


@pytest.fixture(scope="session")
def zipped_csv_processor(tmp_dir, csv_data):
    zipped_csv_processor = ZippedCsvToParqProcessor(
        batch_size=3,
        input_location=LocationConfig(uri=join(tmp_dir, "inputs")),
        output_location=LocationConfig(uri=join(tmp_dir, "outputs")),
        lockfile_location=LocationConfig(uri=tmp_dir),
        csv_seperator=",",
    )
    with open_location(zipped_csv_processor.input_location) as (input_fs, input_root):
        for idx, csv in enumerate(csv_data):
            write_csv(
                data=csv,
                filepath=join(input_root, "csv_data", f"data{idx}.csv"),
                file_system=input_fs,
            )
        shutil.make_archive(
            join(input_root, "data"), "zip", join(input_root, "csv_data")
        )
        input_fs.rm(join(input_root, "csv_data"), recursive=True)
    with open_location(zipped_csv_processor.output_location) as (
        output_fs,
        output_root,
    ):
        output_fs.mkdir(output_root)

    return zipped_csv_processor


@pytest.mark.parametrize(
    "input_file_list, changed_files_dict, force, expected_batches",
    [
        (
            ["file1", "file2", "file3", "file4", "file5"],
            {
                "inputs": {
                    "file1": True,
                    "file2": False,
                    "file3": True,
                    "file4": False,
                    "file5": True,
                },
                "outputs": {
                    "output1": True,
                    "output2": True,
                    "output3": False,
                    "output4": False,
                    "output5": True,
                },
            },
            False,
            [{"inputs": ["file1", "file3", "file5"]}],
        ),
        (
            ["file1", "file2", "file3", "file4", "file5"],
            {
                "inputs": {
                    "file1": True,
                    "file2": False,
                    "file3": True,
                    "file4": False,
                    "file5": True,
                },
                "outputs": {
                    "output1": True,
                    "output2": True,
                    "output3": False,
                    "output4": False,
                    "output5": True,
                },
            },
            True,
            [
                {"inputs": ["file1", "file2", "file3"]},
                {"inputs": ["file4", "file5"]},
            ],
        ),
    ],
)
def test_generate_batches(
    zipped_csv_processor,
    input_file_list,
    changed_files_dict,
    force,
    expected_batches,
):
    actual_batches = zipped_csv_processor.generate_batches(
        input_file_list, changed_files_dict, force=force
    )
    assert actual_batches == expected_batches


def test_process(csv_data, tmp_dir, zipped_csv_processor):
    batch = {"inputs": ["data.zip"]}
    result = zipped_csv_processor.process(batch)

    assert "inputs" in result
    assert "outputs" in result
    assert len(result["outputs"]) == 5

    with open_location(zipped_csv_processor.output_location) as (
        output_fs,
        output_root,
    ):
        parquet_files = list_dir(
            path=output_root, file_system=output_fs, return_full_path=True
        )

        for parquet_file in parquet_files:
            data_frame = read_parquet(filepath=parquet_file, file_system=output_fs)
            assert len(data_frame) == 20
            assert "id" in data_frame.columns and "name" in data_frame.columns


def test_run_process(csv_data, tmp_dir, zipped_csv_processor):
    lock_files = []
    for i in range(2):
        zipped_csv_processor.run_process()

        with open_location(zipped_csv_processor.lockfile_location) as (
            lockfile_fs,
            lockfile_root,
        ):
            lock_data = read_yaml(
                filepath=join(lockfile_root, "lock.yaml"), file_system=lockfile_fs
            )
            lock_files.append(lock_data)
            assert len(lock_data["inputs"]) == 1
            assert len(lock_data["outputs"]) == 5

    assert lock_files[0] == lock_files[1]
