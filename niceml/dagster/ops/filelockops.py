"""module for dagster ops regarding filelocks"""
import json

from dagster import op, OpExecutionContext
from hydra.utils import instantiate, ConvertMode

from niceml.config.hydra import HydraMapField
from niceml.utilities.readwritelock import FileLock


@op(config_schema=dict(filelock_dict=HydraMapField(FileLock)))
def acquire_locks(context: OpExecutionContext):
    """op for acquiring locks"""
    op_config = json.loads(json.dumps(context.op_config))
    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)
    filelock_dict = instantiated_op_config["filelock_dict"]
    for filelock in filelock_dict.values():
        filelock.acquire()
    return filelock_dict


@op
def release_locks(_: OpExecutionContext, filelock_dict: dict):
    """op for releasing locks"""
    for filelock in filelock_dict.values():
        filelock.release()


@op(config_schema=dict(filelock_dict=HydraMapField(FileLock)))
def clear_locks(context: OpExecutionContext):
    """op for clearing locks"""
    op_config = json.loads(json.dumps(context.op_config))
    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)
    filelock_dict = instantiated_op_config["filelock_dict"]
    for filelock in filelock_dict.values():
        filelock.force_delete()
