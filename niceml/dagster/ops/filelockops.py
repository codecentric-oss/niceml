"""module for dagster ops regarding filelocks"""
from typing import Dict

from dagster import op, OpExecutionContext, Config
from hydra.utils import instantiate, ConvertMode

from niceml.config.hydra import create_hydra_map_field
from niceml.utilities.readwritelock import FileLock


class LocksConfig(Config):
    file_lock_dict: dict = create_hydra_map_field(
        target_class=FileLock, alias="file_lock_dict"
    )

    @property
    def file_locks(self) -> Dict[str, FileLock]:
        return instantiate(self.file_lock_dict, _convert_=ConvertMode.ALL)


@op
def acquire_locks(context: OpExecutionContext, config: LocksConfig):
    """op for acquiring locks"""
    for filelock in config.file_locks.values():
        filelock.acquire()
    return config.file_locks


@op
def release_locks(_: OpExecutionContext, filelock_dict: dict):
    """op for releasing locks"""
    for filelock in filelock_dict.values():
        filelock.release()


@op
def clear_locks(context: OpExecutionContext, config: LocksConfig):
    """op for clearing locks"""
    for filelock in config.file_locks.values():
        filelock.force_delete()
