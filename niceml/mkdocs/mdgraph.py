"""Module for generating a graph in mkdocs"""
from dagster import JobDefinition


def get_graph_md(job: JobDefinition) -> str:
    """Creates a graph as str with material for mkdocs"""
    deps = job.graph.dependencies
    graph_str = ""
    for key, value in deps.items():
        for _, val2 in value.items():
            graph_str += f"  {val2.node} --> {key.name};\n"
    if len(graph_str) == 0:
        return ""

    graph_str = "``` mermaid\ngraph LR\n" + graph_str
    graph_str += "```"
    return graph_str
