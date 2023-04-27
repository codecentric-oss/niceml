"""Repository of ccmlops pipelines."""
from typing import List

from niceml.dagster.jobs.jobs import (
    job_copy_exp,
    job_data_generation,
    job_eval,
    job_train,
)
from dagster import JobDefinition, repository


def get_job_list() -> List[JobDefinition]:
    """returns a list of all niceml jobs"""
    return [job_train, job_eval, job_copy_exp, job_data_generation]


@repository
def ccmlops_repository() -> List[JobDefinition]:
    """returns a list of all niceml jobs"""
    return get_job_list()
