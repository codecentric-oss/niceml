from typing import List

from niceml.dagster.jobs.repository import get_job_list
from niceml.mkdocs.mdgraph import get_graph_md


def test_get_graph_md():
    job_list: List = get_job_list()
    for cur_job in job_list:
        md_graph = get_graph_md(cur_job)
        if len(md_graph) > 0:
            assert md_graph.startswith("```")
            assert md_graph.endswith("```")
            assert "mermaid" in md_graph
            assert "graph LR" in md_graph
            assert "-->" in md_graph
