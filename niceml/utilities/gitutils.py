"""Module for git utils"""
import os
import subprocess
from importlib import import_module
from typing import List, Union

from niceml.experiments.experimentcontext import ExperimentContext


class NoGitHashAvailableError(Exception):
    """Exception for when no git hash is available"""


def get_git_revision_hash(path: str = "."):
    """Get the git revision hash of the repository located in the path"""
    try:
        git_commit_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=path
        )
    except Exception as exc:
        raise NoGitHashAvailableError(
            f"Folder seems to be no git repo: {path}"
        ) from exc

    return git_commit_hash.decode("utf-8")


def get_module_dir(module_name: str):
    """Get the directory of a module"""
    module = import_module(module_name)
    return os.path.dirname(module.__file__)


def get_git_revision_of_module(module_name: str):
    """Get the git revision hash of a module"""
    mod_dir = get_module_dir(module_name)
    return get_git_revision_hash(mod_dir)


def produce_git_version_yaml(
    exp_context: ExperimentContext,
    filepath: str,
    git_dirs: Union[str, List[str], None] = None,
    git_modules: Union[str, List[str], None] = None,
):
    """Produce a yaml file with the git hashes of the given directories and modules"""
    if git_modules is None:
        git_modules = []
    if git_dirs is None:
        git_dirs = []

    output_versions = {}
    for cur_dir in git_dirs:
        try:
            output_versions[cur_dir] = get_git_revision_hash(cur_dir)
        except NoGitHashAvailableError:
            output_versions[cur_dir] = "NoVersionAvailable"
    for mod in git_modules:
        try:
            output_versions[mod] = get_git_revision_of_module(mod)
        except NoGitHashAvailableError:
            output_versions[mod] = "NoVersionAvailable"
    exp_context.write_yaml(output_versions, filepath)
