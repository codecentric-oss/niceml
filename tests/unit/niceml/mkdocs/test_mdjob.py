from typing import List

from niceml.dagster.jobs.repository import get_job_list
from niceml.mkdocs.mdjob import get_job_md


def test_get_job_md():
    job_list: List = get_job_list()
    for cur_job in job_list:
        md_job = get_job_md(cur_job)
        assert md_job.startswith("##")
