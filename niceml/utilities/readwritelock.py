"""Module for Read/Write lock for fsspec filesystems"""
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem

from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_fs_path,
    open_location,
)


class FileLock(ABC):
    """Abstract base class for file locks."""

    def __init__(
        self,
        retry_time: float = 10,
        timeout: float = 172800,
    ):
        self.retry_time = retry_time
        self.timeout = timeout
        self.is_acquired: bool = False

    @abstractmethod
    def acquire(self):
        """Acquire the lock"""

    @abstractmethod
    def release(self):
        """Release the lock"""

    @abstractmethod
    def force_delete(self):
        """Force delete the lock"""

    def __enter__(self):
        """context manager enter method"""
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """context manager exit method"""
        self.release()


class WriteLock(FileLock):
    """Write lock for fsspec filesystems."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        path_config: Union[LocationConfig, Dict[str, Any]],
        write: bool = False,
        retry_time: float = 10,
        timeout: float = 172800,
        write_lock_name: str = "write.lock",
        read_lock_name: str = "read.lock",
    ):
        if write_lock_name == read_lock_name:
            raise ValueError("write_lock_name and read_lock_name must be different")
        super().__init__(retry_time, timeout)
        self.path_config = path_config
        self.write = write
        self.write_lock_name = write_lock_name
        self.read_lock_name = read_lock_name

    def acquire(self):
        """Acquire the lock"""
        if self.is_acquired:
            return
        with open_location(self.path_config) as (cur_fs, root_path):
            start_time = time.monotonic()
            while True:
                write_lock_path = join_fs_path(cur_fs, root_path, self.write_lock_name)
                if is_lock_file_acquirable(write_lock_path, cur_fs):
                    acquire_lock_file(write_lock_path, cur_fs)
                    self.is_acquired = True
                    break
                if time.monotonic() - start_time > self.timeout:
                    raise TimeoutError(
                        f"Timeout while acquiring write lock {write_lock_path}"
                    )
                time.sleep(self.retry_time)
            while True:
                read_lock_path = join_fs_path(cur_fs, root_path, self.read_lock_name)
                if is_lock_file_acquirable(read_lock_path, cur_fs):
                    break
                if time.monotonic() - start_time > self.timeout:
                    self.release()
                    raise TimeoutError(
                        f"Timeout while acquiring read lock {read_lock_path}"
                    )
                time.sleep(self.retry_time)

    def force_delete(self):
        """Force delete the lock"""
        self.is_acquired = False
        with open_location(self.path_config) as (cur_fs, root_path):
            write_lock_path = join_fs_path(cur_fs, root_path, self.write_lock_name)
            release_lock_file(write_lock_path, cur_fs)

    def release(self):
        """Release the lock"""
        if self.is_acquired:
            with open_location(self.path_config) as (cur_fs, root_path):
                write_lock_path = join_fs_path(cur_fs, root_path, self.write_lock_name)
                release_lock_file(write_lock_path, cur_fs)
                self.is_acquired = False


class ReadLock(FileLock):
    """Read lock for fsspec filesystems."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        path_config: Union[LocationConfig, Dict[str, Any]],
        retry_time: float = 10,
        timeout: float = 172800,
        write_lock_name: str = "write.lock",
        read_lock_name: str = "read.lock",
    ):
        if write_lock_name == read_lock_name:
            raise ValueError("write_lock_name and read_lock_name must be different")
        super().__init__(retry_time, timeout)
        self.path_config = path_config
        self.write_lock_name = write_lock_name
        self.read_lock_name = read_lock_name

    def acquire(self):
        """Acquire the lock"""
        if self.is_acquired:
            return
        with open_location(self.path_config) as (cur_fs, root_path):
            start_time = time.monotonic()
            while True:
                write_lock_path = join_fs_path(cur_fs, root_path, self.write_lock_name)
                if is_lock_file_acquirable(write_lock_path, cur_fs):
                    break
                if time.monotonic() - start_time > self.timeout:
                    raise TimeoutError(
                        f"Timeout while acquiring write lock {write_lock_path}"
                    )
                time.sleep(self.retry_time)
            read_lock_path = join_fs_path(cur_fs, root_path, self.read_lock_name)
            increase_lock_file_usage(read_lock_path, cur_fs)
            self.is_acquired = True

    def force_delete(self):
        """Force delete the lock"""
        self.is_acquired = False
        with open_location(self.path_config) as (cur_fs, root_path):
            write_lock_path = join_fs_path(cur_fs, root_path, self.read_lock_name)
            release_lock_file(write_lock_path, cur_fs)

    def release(self):
        """Release the lock"""
        if self.is_acquired:
            with open_location(self.path_config) as (cur_fs, root_path):
                read_lock_path = join_fs_path(cur_fs, root_path, self.read_lock_name)
                decrease_lock_file_usage(read_lock_path, cur_fs)
                self.is_acquired = False


def is_lock_file_acquirable(
    lock_file_path: str, file_system: Optional[AbstractFileSystem] = None
) -> bool:
    """Check if the lock file is available."""
    file_system = file_system or LocalFileSystem()
    if file_system.exists(lock_file_path):
        return False
    return True


def acquire_lock_file(
    lock_file_path: str, file_system: Optional[AbstractFileSystem]
) -> None:
    """Acquire the lock file."""
    file_system = file_system or LocalFileSystem()
    if not is_lock_file_acquirable(lock_file_path, file_system):
        raise RuntimeError(f"Lock file {lock_file_path} is not available.")
    file_system.touch(lock_file_path)


def release_lock_file(
    lock_file_path: str, file_system: Optional[AbstractFileSystem]
) -> None:
    """Release the lock file."""
    file_system = file_system or LocalFileSystem()
    if not file_system.exists(lock_file_path):
        logger = logging.getLogger(__name__)
        logger.warning(f"Lock file {lock_file_path} does not exist.")
    else:
        file_system.rm(lock_file_path)


def increase_lock_file_usage(
    lock_file_path: str, file_system: Optional[AbstractFileSystem]
) -> None:
    """Increase the lock file usage."""
    file_system = file_system or LocalFileSystem()
    if not file_system.exists(lock_file_path):
        current_usage: int = 0
    else:
        with file_system.open(lock_file_path, "r") as file:
            current_usage = int(file.read())
    with file_system.open(lock_file_path, "w") as file:
        file.write(str(current_usage + 1))


def decrease_lock_file_usage(
    lock_file_path: str, file_system: Optional[AbstractFileSystem]
) -> None:
    """Decrease the lock file usage."""
    file_system = file_system or LocalFileSystem()
    if not file_system.exists(lock_file_path):
        current_usage: int = 0
    else:
        with file_system.open(lock_file_path, "r") as file:
            current_usage = int(file.read())
    if current_usage > 1:
        with file_system.open(lock_file_path, "w") as file:
            file.write(str(current_usage - 1))
    else:
        file_system.rm(lock_file_path)
