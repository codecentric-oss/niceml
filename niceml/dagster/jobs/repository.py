"""Repository of niceml pipelines."""
from typing import List

from dagster import JobDefinition, repository, Definitions

from niceml.dagster.jobs.jobs import job_train_cls


def get_job_list() -> List[JobDefinition]:
    """returns a list of all niceml jobs"""
    return [job_train_cls]


defs = Definitions(jobs=get_job_list())
