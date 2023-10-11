"""Module for generating a graph in mkdocs"""
from dagster import JobDefinition, DependencyDefinition, MultiDependencyDefinition


def get_graph_md(job: JobDefinition) -> str:
    """Creates a graph as str with material for mkdocs"""
    deps = job.graph.dependencies
    graph_str = ""
    for key, value in deps.items():
        for _, val2 in value.items():
            if isinstance(val2, DependencyDefinition):
                graph_str += f"  {val2.node} --> {key.name};\n"
            elif isinstance(val2, MultiDependencyDefinition):
                for dependency in val2.dependencies:
                    graph_str += f"  {dependency.node} --> {key.name};\n"
            else:
                raise AttributeError("'val2' is not of expected type.")
    if len(graph_str) == 0:
        return ""

    graph_str = "``` mermaid\ngraph LR\n" + graph_str
    graph_str += "```"
    return graph_str
