"""Module containing all dagster jobs"""

from dagster import JobDefinition

from niceml.config.hydra import hydra_conf_mapping_factory
from niceml.dagster.jobs.graphs import (
    graph_train,
    graph_data_generation,
    graph_eval,
    graph_copy_exp,
    graph_clearlocks,
)

# TODO: remove hydra_conf_mapping_factory
job_data_generation = JobDefinition(
    graph_def=graph_data_generation, config=hydra_conf_mapping_factory()
)
job_train = JobDefinition(graph_def=graph_train, config=hydra_conf_mapping_factory())
job_eval = JobDefinition(graph_def=graph_eval, config=hydra_conf_mapping_factory())
job_copy_exp = JobDefinition(
    graph_def=graph_copy_exp, config=hydra_conf_mapping_factory()
)
job_clearlocks = JobDefinition(
    graph_def=graph_clearlocks, config=hydra_conf_mapping_factory()
)
