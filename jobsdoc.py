"""generates a markdownfile for schemas"""
from typing import List

import mkdocs_gen_files

from niceml.dagster.jobs.repository import get_job_list
from niceml.mkdocs.mdjob import get_job_md

with mkdocs_gen_files.open("jobsdoc.md", "w") as md_file:
    print("# Overview of DagsterJobs\n\n", file=md_file)
    job_list: List = get_job_list()
    for cur_job in job_list:
        job_md = get_job_md(cur_job)
        print(job_md, file=md_file)
