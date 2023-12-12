# pylint: disable=duplicate-code

import time
from tempfile import TemporaryDirectory

import pytest

from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_fs_path,
    open_location,
    join_location_w_path,
)
from niceml.utilities.readwritelock import (
    ReadLock,
    WriteLock,
    is_lock_file_acquirable,
    acquire_lock_file,
    release_lock_file,
    increase_lock_file_usage,
    decrease_lock_file_usage,
)


@pytest.fixture()
def fs_path_config():
    with TemporaryDirectory() as tmp_dir:
        yield LocationConfig(uri=tmp_dir)


def test_read_lock(fs_path_config):
    read_lock = ReadLock(fs_path_config)
    assert read_lock.is_acquirable()
    read_lock.acquire()
    assert not read_lock.is_acquirable()
    time.sleep(1)
    read_lock.release()

    # lock files should not exist anymore after release
    assert read_lock.is_acquirable()


def test_write_lock(fs_path_config):
    write_lock = WriteLock(fs_path_config)
    assert write_lock.is_acquirable()
    write_lock.acquire()
    assert not write_lock.is_acquirable()
    time.sleep(1)
    write_lock.release()

    # lock files should not exist anymore after release
    assert write_lock.is_acquirable()


def test_retry_lock(fs_path_config):
    # create write lock file manually
    with open_location(fs_path_config) as (cur_fs, root_path):
        cur_fs.touch(join_fs_path(cur_fs, root_path, "write.lock"))

    write_lock = WriteLock(fs_path_config, retry_time=0.1, timeout=1)
    start_time = time.monotonic()
    with pytest.raises(TimeoutError):
        write_lock.acquire()
    end_time = time.monotonic()
    assert end_time - start_time >= 1

    # lock file should still exist
    assert not write_lock.is_acquirable()
    write_lock.release()

    # lock files should not be able to delete a lock file, if they have
    # not created the file.
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))


def test_lock_context_manager(fs_path_config):
    with WriteLock(fs_path_config) as rw_lock:
        assert isinstance(rw_lock, WriteLock)
        with open_location(fs_path_config) as (cur_fs, root_path):
            assert cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))
            assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))
        time.sleep(1)

    with ReadLock(fs_path_config) as rw_lock:
        assert isinstance(rw_lock, ReadLock)
        with open_location(fs_path_config) as (cur_fs, root_path):
            assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))
            assert cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))
        time.sleep(1)

    # lock files should not exist anymore after release
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))


def test_raise_timeout_during_read(fs_path_config):
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
    with pytest.raises(TimeoutError):
        write_lock.acquire()
    read_lock2.release()
    write_lock.acquire()
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))
        assert cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))

    write_lock.release()
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))


def test_raise_timeout_during_write(fs_path_config):
    write_lock1 = WriteLock(fs_path_config, retry_time=0.05, timeout=0.5)
    write_lock2 = WriteLock(fs_path_config, retry_time=0.05, timeout=0.5)
    read_lock = ReadLock(fs_path_config, retry_time=0.05, timeout=0.5)

    write_lock1.acquire()
    with pytest.raises(TimeoutError):
        write_lock2.acquire()
    with pytest.raises(TimeoutError):
        read_lock.acquire()

    write_lock1.release()
    read_lock.acquire()
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))

    read_lock.release()
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))


def test_read_lock_force_delete(fs_path_config):
    read_lock1 = ReadLock(fs_path_config, retry_time=0.05, timeout=0.5)
    read_lock1.acquire()
    read_lock2 = ReadLock(fs_path_config, retry_time=0.05, timeout=0.5)
    read_lock2.acquire()
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))
    read_lock1.force_delete()
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "read.lock"))
    assert read_lock2.is_acquirable()
    assert read_lock2.is_acquired is True
    read_lock2.release()


def test_write_lock_force_delete(fs_path_config):
    write_lock1 = WriteLock(fs_path_config, retry_time=0.05, timeout=0.5)
    write_lock2 = WriteLock(fs_path_config, retry_time=0.05, timeout=0.5)
    write_lock1.acquire()
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))
    write_lock2.force_delete()
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert not cur_fs.exists(join_fs_path(cur_fs, root_path, "write.lock"))
    assert write_lock1.is_acquirable()
    assert write_lock1.is_acquired is True
    write_lock1.release()


def test_is_lock_file_acquirable(fs_path_config):
    with open_location(fs_path_config) as (cur_fs, root_path):
        lock_file_path = join_fs_path(cur_fs, root_path, "write.lock")
    assert is_lock_file_acquirable(lock_file_path, cur_fs) is True
    assert is_lock_file_acquirable(lock_file_path) is True

    with open_location(fs_path_config) as (cur_fs, root_path):
        cur_fs.touch(lock_file_path)
    assert is_lock_file_acquirable(lock_file_path, cur_fs) is False
    assert is_lock_file_acquirable(lock_file_path) is False


def test_acquire_lock_file(fs_path_config):
    with open_location(fs_path_config) as (cur_fs, root_path):
        lock_file_path = join_fs_path(cur_fs, root_path, "write.lock")
        assert cur_fs.exists(lock_file_path) is False

    acquire_lock_file(lock_file_path, cur_fs)
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert cur_fs.exists(lock_file_path) is True

    with pytest.raises(RuntimeError):
        acquire_lock_file(lock_file_path)


def test_release_lock_file(fs_path_config):
    with open_location(fs_path_config) as (cur_fs, root_path):
        lock_file_path = join_fs_path(cur_fs, root_path, "write.lock")
        cur_fs.touch(lock_file_path)

    release_lock_file(lock_file_path, cur_fs)
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert cur_fs.exists(lock_file_path) is False

    release_lock_file(lock_file_path)


def test_lock_file_usage(fs_path_config):
    with open_location(fs_path_config) as (cur_fs, root_path):
        lock_file_path = join_fs_path(cur_fs, root_path, "read.lock")

    # increase
    increase_lock_file_usage(lock_file_path, cur_fs)
    with cur_fs.open(lock_file_path, "r") as file:
        assert file.read() == "1"
    increase_lock_file_usage(lock_file_path, None)
    with cur_fs.open(lock_file_path, "r") as file:
        assert file.read() == "2"

    # decrease
    decrease_lock_file_usage(lock_file_path, cur_fs)
    with cur_fs.open(lock_file_path, "r") as file:
        assert file.read() == "1"
    decrease_lock_file_usage(lock_file_path)
    with open_location(fs_path_config) as (cur_fs, root_path):
        assert cur_fs.exists(lock_file_path) is False
