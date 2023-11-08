"""Module for generating a graph in mkdocs"""
from dagster import JobDefinition, DependencyDefinition, MultiDependencyDefinition


def get_graph_md(job: JobDefinition) -> str:
    """Creates a graph as str with material for mkdocs"""
    deps = job.graph.dependencies
    graph_str = ""
    for node, node_dependencies in deps.items():
        for _, dependencies in node_dependencies.items():
            if isinstance(dependencies, DependencyDefinition):
                graph_str += f"  {dependencies.node} --> {node.name};\n"
            elif isinstance(dependencies, MultiDependencyDefinition):
                for dependency in dependencies.dependencies:
                    graph_str += f"  {dependency.node} --> {node.name};\n"
            else:
                raise AttributeError("'dependencies' is not of expected type.")
    if len(graph_str) == 0:
        return ""

    graph_str = "``` mermaid\ngraph LR\n" + graph_str
    graph_str += "```"
    return graph_str
