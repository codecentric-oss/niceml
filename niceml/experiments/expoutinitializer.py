"""Module for expout initializer"""
from os.path import basename, dirname, join
from typing import List, Optional

from pydantic import BaseModel, Field

from niceml.config.config import InitConfig, Configurable
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.utilities.copyutils import CopyInfo
from niceml.utilities.fsspec.locationutils import open_location
from niceml.utilities.gitutils import produce_git_version_yaml


class ExpOutInitializer(Configurable):
    """This class creates the first folder and files for an experiment"""

    def __init__(
        self,
        git_dirs: Optional[List[str]] = None,
        git_modules: Optional[List[str]] = None,
        environment: Optional[dict] = None,
        exp_type: str = "",
        exp_name: str = "",
        description: str = "",
        exp_prefix: str = "",
        copy_info: Optional[CopyInfo] = None,
    ):
        """
        This class creates the first folder and files for an experiment
        Args:
            exp_prefix: Experiment prefix which is stored in the experiment info file
            git_dirs: List of git directories of which the commit hash should be stored
            git_modules: List of git modules of which the commit hash should be stored
            environment: Environment dictionary which is stored in the experiment info file
            exp_type:Experiment type which is stored in the experiment info file
            exp_name: Experiment name which is stored in the experiment info file
            description: Experiment description which is stored in the experiment info file
            copy_info:CopyInfo object which copies files to the experiment folder
        """
        self.exp_prefix: str = exp_prefix
        self.copy_info: CopyInfo = copy_info
        self.description: str = description
        self.exp_name: str = exp_name
        self.exp_type: str = exp_type
        self.environment: dict = environment or {}
        self.git_modules: List[str] = git_modules or []
        self.git_dirs: List[str] = git_dirs or []

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
