"""Module which contains factory methods for creating experiment data objects"""
from typing import Optional

from niceml.data.dataloaders.dfloaders import SimpleDfLoader
from niceml.data.dataloaders.imageloaders import SimpleImageLoader
from niceml.data.storages.fsspecstorage import FSSpecStorage
from niceml.data.storages.localstorage import LocalStorage
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.expdatastorageloader import create_expdata_from_storage
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.experimentdata import ExperimentData


def create_expdata_from_local_storage(
    exp_path: str,
    storage: Optional[StorageInterface] = None,
) -> ExperimentData:
    """Creates and loads an experiment data with the given path"""
    if storage is None:
        storage = LocalStorage()
    df_loader = SimpleDfLoader(storage, working_dir=exp_path)
    image_loader = SimpleImageLoader(storage, working_dir=exp_path)
    return create_expdata_from_storage(
        exp_path, storage, image_loader=image_loader, df_loader=df_loader
    )


def create_expdata_from_expcontext(exp_context: ExperimentContext) -> ExperimentData:
    """Creates and loads an experiment data with the given experiment context"""
    storage = FSSpecStorage(exp_context.fs_config)
    return create_expdata_from_local_storage(storage=storage, exp_path="")
