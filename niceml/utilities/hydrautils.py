"""module for utilities related to hydra"""
from os.path import dirname, basename, splitext
from typing import Union, Optional, List

import yaml
import networkx as nx

from niceml.utilities.ioutils import read_yaml, find_and_read_file


def build_import_graph(
    root_file: str, search_paths: Optional[List[str]] = None
) -> nx.DiGraph:
    """Builds a directed graph of the import hierarchy of the given root file.
    Args:
         root_file: Path to the yaml-root file of the import hierarchy
         search_paths: List of paths to search for imported yaml files
    Returns:
         import_graph: Directed graph of the import hierarchy
    """
    # Initialize the import graph
    import_graph = nx.DiGraph()
    search_paths = search_paths or []

    # Get the root file's directory and load its configuration
    root_config_path, root_config = find_and_read_file(
        root_file, search_paths=search_paths, read_func=read_yaml
    )

    # Add the root file to the import graph
    import_graph.add_node(root_file)
    search_paths.append(dirname(root_config_path))
    # Traverse the import hierarchy recursively
    import_graph = traverse_import_hierarchy(
        root_config, root_file, import_graph, search_paths=search_paths
    )
    return import_graph


def traverse_import_hierarchy(
    config: dict, config_file: str, import_graph: nx.DiGraph, search_paths: List[str]
):
    """Traverses the import hierarchy of the given configuration file and adds the import edges to the import graph."""
    if "defaults" in config:
        for import_path in config["defaults"]:
            # Build the absolute path to the imported configuration file
            import_path = parse_defaults_content(import_path)
            if import_path == "_self_":
                continue
            import_file, import_conf = find_and_read_file(
                import_path, search_paths=search_paths, read_func=read_yaml
            )

            # Add the imported configuration file to the import graph
            import_graph.add_node(import_file)
            import_graph.add_edge(config_file, import_file)

            # Load and traverse the imported configuration file
            import_config = yaml.safe_load(open(import_file))
            cur_search_paths = search_paths.copy() + [dirname(import_file)]
            traverse_import_hierarchy(
                import_config, import_file, import_graph, search_paths=cur_search_paths
            )
    return import_graph


def nx_to_mermaid(nx_graph: nx.DiGraph):
    """Converts a networkx graph to a Mermaid.js graph string."""
    # Initialize the Mermaid.js graph string
    mermaid_graph = "graph LR;\n"

    for source, target in nx_graph.edges():
        source_text = basename(splitext(source)[0])
        target_text = basename(splitext(target)[0])
        mermaid_graph += f"{source}({source_text}) --> {target}({target_text});\n"

    return mermaid_graph


def parse_defaults_content(entry: Union[dict, str]) -> str:
    """Parses the content of a defaults entry and returns the corresponding path."""
    if isinstance(entry, dict):
        if len(entry) != 1:
            raise ValueError("Only one key allowed in defaults entry")
        main_val = list(entry.keys())[0]
        additional_val = entry[main_val]

    else:
        main_val = entry
        additional_val = ""

    if "@" in main_val:
        main_val = main_val.split("@")[0]

    if len(additional_val) > 0:
        return_val = "/".join([main_val, additional_val])
    else:
        return_val = main_val
    return return_val
