# pylint: disable=duplicate-code

import time
from tempfile import TemporaryDirectory

import pytest

from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_fs_path,
    open_location,
)
from niceml.utilities.readwritelock import ReadLock, WriteLock


@pytest.fixture()
def fs_path_config():
    with TemporaryDirectory() as tmp_dir:
        yield LocationConfig(uri=tmp_dir)


def test_read_lock(fs_path_config):
    rw_lock = ReadLock(fs_path_config)
    rw_lock.acquire()
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))
    time.sleep(1)
    rw_lock.release()

    # lock files should not exist anymore after release
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))


def test_write_lock(fs_path_config):
    write_lock = WriteLock(fs_path_config)
    write_lock.acquire()
    time.sleep(1)
    write_lock.release()

    # lock files should not exist anymore after release
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))


def test_read_write_lock(fs_path_config):
    write_lock = WriteLock(fs_path_config, write=True)
    write_lock.acquire()
    time.sleep(1)
    write_lock.release()

    # lock files should not exist anymore after release
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))


def test_retry_lock(fs_path_config):
    # create read lock file manually
    with open_location(fs_path_config) as (cur_fs, root_path):
        cur_fs.touch(join_fs_path(cur_fs, root_path, "write.lock"))

    write = WriteLock(fs_path_config, retry_time=0.1, timeout=1)
    start_time = time.monotonic()
    with pytest.raises(TimeoutError):
        write.acquire()
    end_time = time.monotonic()
    assert end_time - start_time >= 1

    # lock file should still exist
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))
    write.release()

    # lock files should not be able to be released from the rw_lock
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))


def test_context_manager(fs_path_config):
    with WriteLock(fs_path_config) as rw_lock:
        assert isinstance(rw_lock, WriteLock)
        with open_location(fs_path_config) as (cur_fs, root_path):
            assert cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))
        time.sleep(1)

    # lock files should not exist anymore after release
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))


def test_raise_write_during_read(fs_path_config):
    read_lock1 = ReadLock(fs_path_config, retry_time=0.05, timeout=0.5)
    read_lock2 = ReadLock(fs_path_config, retry_time=0.05, timeout=0.5)
    write_lock = WriteLock(fs_path_config, retry_time=0.05, timeout=0.5)

    read_lock1.acquire()
    with pytest.raises(TimeoutError):
        write_lock.acquire()

    read_lock2.acquire()
    with pytest.raises(TimeoutError):
        write_lock.acquire()

    read_lock1.release()
    read_lock2.release()
    write_lock.acquire()
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))
        assert cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))

    write_lock.release()
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))
