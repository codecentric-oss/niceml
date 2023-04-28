import os
from os.path import join
from tempfile import TemporaryDirectory

import pytest
from fsspec.implementations.local import LocalFileSystem

from niceml.utilities.checksums import (
    combine_checksums,
    hex_leading_zeros,
    md5_from_file,
    md5_from_filelist_or_dir,
)


@pytest.fixture
def checksum_tmp_dir() -> str:
    """Creates a temporary directory for testing"""
    with TemporaryDirectory() as tmp_dir:
        yield tmp_dir


def test_md5_from_file(checksum_tmp_dir):
    file_path = join(checksum_tmp_dir, "test_file.txt")
    expected_md5 = "098f6bcd4621d373cade4e832627b4f6"
    with open(file_path, "w") as file:
        file.write("test")

    assert md5_from_file(file_path) == expected_md5


def test_md5_from_filelist_or_dir(checksum_tmp_dir):
    file_system = LocalFileSystem()
    file_list = ["test_dir/test_file1.txt", "test_dir/test_file2.txt", "test_file3.txt"]
    file_list = [join(checksum_tmp_dir, file) for file in file_list]
    os.mkdir(join(checksum_tmp_dir, "test_dir"))

    for file in file_list:
        with open(file, "w", encoding="utf-8") as w_file:
            w_file.write("test")

    result_md5 = md5_from_filelist_or_dir(file_list, file_system)

    expected_md5 = "0x98f6bcd4621d373cade4e832627b4f6"

    assert result_md5 == expected_md5


def test_combine_checksums():
    first_hash = "0x8f6bcd4621d373cade4e832627b4f67"
    second_hash = "0x98f6bcd4621d373cade4e725627b4f6"
    result_checksum = combine_checksums(first_hash, second_hash)
    expected_result = "0x179d719243ce44f673aa640345cfb91"

    assert result_checksum == expected_result


def test_hex_leading_zeros():
    value = 16
    length = 6
    expected_result = "0x0010"

    assert hex_leading_zeros(value, length) == expected_result

    value = 255
    length = 4
    expected_result = "0xff"

    assert hex_leading_zeros(value, length) == expected_result
