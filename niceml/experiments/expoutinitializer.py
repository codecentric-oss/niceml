"""Module for expout initializer"""
from os.path import basename, dirname, join
from typing import List, Optional

from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.utilities.copyutils import CopyInfo
from niceml.utilities.fsspec.locationutils import open_location
from niceml.utilities.gitutils import produce_git_version_yaml


class ExpOutInitializer:
    """This class creates the first folder and files for an experiment"""

    # pylint: disable=too-many-instance-attributes, too-many-arguments, too-few-public-methods
    def __init__(
        self,
        git_dirs: List[str] = None,
        git_modules: List[str] = None,
        copy_info: Optional[CopyInfo] = None,
        environment: Optional[dict] = None,
        exp_name: Optional[str] = None,
        exp_prefix: Optional[str] = None,
        description: Optional[str] = None,
        exp_type: Optional[str] = None,
    ):
        self.copy_info = copy_info
        self.git_dirs: List[str] = git_dirs or []
        self.git_modules: List[str] = git_modules or []
        self.environment = environment or {}
        self.description = description or ""
        self.exp_name: str = exp_name or ""
        self.exp_prefix: str = exp_prefix or ""
        self.exp_type: str = exp_type or ""

    def __call__(self, exp_context: ExperimentContext):

        produce_git_version_yaml(
            exp_context,
            ExperimentFilenames.GIT_VERSIONS,
            self.git_dirs,
            self.git_modules,
        )
        produce_exp_info(
            exp_context,
            ExperimentFilenames.EXP_INFO,
            self.environment,
            description=self.description,
            short_id=exp_context.short_id,
            run_id=exp_context.run_id,
            exp_prefix=self.exp_prefix,
            exp_name=self.exp_name,
            experiment_type=self.exp_type,
        )

        if self.copy_info is not None:
            with open_location(exp_context.fs_config) as (exp_fs, root_exp_path):
                external_infos_folder: str = join(
                    root_exp_path, ExperimentFilenames.EXTERNAL_INFOS
                )
                self.copy_info.copy_to_filesystem(exp_fs, external_infos_folder)


def produce_exp_info(  # pylint: disable=too-many-arguments
    exp_context: ExperimentContext,
    filepath: str,
    environment: dict,
    description: str,
    short_id: str,
    run_id: str,
    exp_name: str,
    experiment_type: str = "",
    exp_prefix: Optional[str] = None,
):
    """This function creates the experiment info file
    and stores it within the experiment folder"""
    exp_info = ExperimentInfo(
        experiment_name=exp_name,
        experiment_prefix=exp_prefix,
        experiment_type=experiment_type,
        run_id=run_id,
        short_id=short_id,
        environment=environment,
        description=description,
        exp_dir=basename(dirname(filepath)),
    )
    out_dict = exp_info.as_save_dict()
    exp_context.write_yaml(out_dict, filepath)
