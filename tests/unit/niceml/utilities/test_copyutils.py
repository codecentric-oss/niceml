from os.path import join
from tempfile import TemporaryDirectory

import pytest
from fsspec.implementations.local import LocalFileSystem

from niceml.utilities.checksums import md5_from_file
from niceml.utilities.copyutils import (
    CopyFileInfo,
    CopyInfo,
    filter_for_required,
    process_copy_files,
)


@pytest.fixture
def source_tmp_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp


@pytest.fixture
def target_fs():
    return LocalFileSystem()


@pytest.fixture
def target_tmp_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp


@pytest.fixture
def source_fs():
    return LocalFileSystem()


def test_copy_to_filesystem(source_fs, target_fs, source_tmp_dir, target_tmp_dir):
    source_file_content = b"Hello, world!"
    source_file_path = "example/source.txt"
    source_fs.mkdir(join(source_tmp_dir, "example"))
    with source_fs.open(join(source_tmp_dir, source_file_path), "wb") as source_file:
        source_file.write(source_file_content)

    copy_info = CopyInfo({"uri": source_tmp_dir}, copy_filelist=[source_file_path])
    copy_info.copy_to_filesystem(target_fs, join(target_tmp_dir, "example"))
    assert target_fs.exists(join(target_tmp_dir, source_file_path))
    with target_fs.open(join(target_tmp_dir, source_file_path), "rb") as file:
        assert file.read() == source_file_content


def test_copy_fileinfo(source_fs, target_fs, source_tmp_dir, target_tmp_dir):
    source_file_content = b"Hello, world!"
    source_file_path = "example/source.txt"
    source_fs.mkdir(join(source_tmp_dir, "example"))
    with source_fs.open(join(source_tmp_dir, source_file_path), "wb") as source_file:
        source_file.write(source_file_content)

    copy_info = CopyFileInfo(
        input_location={"uri": join(source_tmp_dir, source_file_path)},
        output_location={"uri": join(target_tmp_dir, source_file_path)},
        checksum=md5_from_file(join(source_tmp_dir, source_file_path), source_fs),
    )

    copy_file_list = filter_for_required([copy_info])
    assert len(copy_file_list) == 1

    process_copy_files(copy_file_list)
    assert target_fs.exists(join(target_tmp_dir, source_file_path))
    with target_fs.open(join(target_tmp_dir, source_file_path), "rb") as file:
        assert file.read() == source_file_content
