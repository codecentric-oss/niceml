"""module for dagster ops regarding filelocks"""

from dagster import Config
from dagster import op, OpExecutionContext

from niceml.config.config import MapInitConfig
from niceml.utilities.readwritelock import FileLock


class LocksConfig(Config):
    file_lock_dict: MapInitConfig = MapInitConfig.create_config_field(
        target_class=FileLock,
    )


@op
def acquire_locks(context: OpExecutionContext, config: LocksConfig):
    """op for acquiring locks"""
    filelock_dict = config.file_lock_dict.instantiate()
    for filelock in filelock_dict.values():
        filelock.acquire()
    return filelock_dict


@op
def release_locks(_: OpExecutionContext, filelock_dict: dict):
    """op for releasing locks"""
    for filelock in filelock_dict.values():
        filelock.release()


@op
def clear_locks(context: OpExecutionContext, config: LocksConfig):
    """op for clearing locks"""
    for filelock in config.file_lock_dict.instantiate().values():
        filelock.force_delete()
