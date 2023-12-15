"""Repository of niceml pipelines."""
from typing import List

from dagster import JobDefinition, repository

from niceml.dagster.jobs.jobs import (
    job_train,
)


def get_job_list() -> List[JobDefinition]:
    """returns a list of all niceml jobs"""
    return [job_train]


@repository
def niceml_repository() -> List[JobDefinition]:
    """returns a list of all niceml jobs"""
    return get_job_list()
