"""Module for generating mkdocs str for jobs"""
from typing import List

from dagster.core.definitions import NodeDefinition

from niceml.mkdocs.mdgraph import get_graph_md
from niceml.mkdocs.mdop import get_md_op
from dagster import JobDefinition


def get_job_md(job: JobDefinition, include_graph: bool = True) -> str:
    """creates the job markdown"""
    job_md: str = f"## Job: `{job.name}`\n\n"

    job_md += job.__doc__ + "\n\n"
    if include_graph:
        graph_md = get_graph_md(job)
        if len(graph_md) > 0:
            job_md += graph_md + "\n\n"
    op_list: List[NodeDefinition] = get_ops_from_job(job)
    for cur_op in op_list:
        job_md += get_md_op(cur_op)

    return job_md


def get_ops_from_job(job: JobDefinition) -> List[NodeDefinition]:
    """Returns all ops from job"""
    return job.all_node_defs
