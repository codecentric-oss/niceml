"""Module containing the base experiment schema"""
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.experiments.schemas.expmember import FolderMember, LogCsvMember
from niceml.experiments.schemas.yamlexpmember import ExpInfoMember


class BaseExperimentSchema:  # pylint: disable=too-few-public-methods
    """base experiment schema for subclassing"""

    exp_info = ExpInfoMember()
    log_data = LogCsvMember()
    model_folder = FolderMember(
        ExperimentFilenames.MODELS_FOLDER,
        required=True,
        min_required_files=1,
        extensions=[".hdf5"],
        description="This folder contains all trained models",
    )
