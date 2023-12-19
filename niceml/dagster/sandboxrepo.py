from typing import List

from dagster import (
    job,
    JobDefinition,
    repository,
    op,
    Config,
    config_mapping,
    RunConfig,
    graph,
)
from pydantic import Field


class ConstantConfig(Config):
    value: int = Field(default=5, description="The value to return.")


@op
def return_constant(config: ConstantConfig):
    return config.value


class AddOneConfig(Config):
    value: int = Field(default=5, description="The value to add one to.")


@op
def add_one(config: AddOneConfig, arg):
    return arg + config.value


class BaseSimplifiedConfig(Config):
    simplified_param: int = Field(default=5, description="All the values.")
    value: int = Field(default=8, description="Nothing to configure.")


class SimplifiedConfig1(BaseSimplifiedConfig):
    simplified_param: int = Field(default=1, description="Simplified vals 1.")


class SimplifiedConfig2(BaseSimplifiedConfig):
    simplified_param: int = Field(default=2, description="Simplified vals 2.")


def get_run_conf_from_simplified_config(val) -> RunConfig:
    return RunConfig(
        ops={
            "add_one": AddOneConfig(value=val.simplified_param),
            "return_constant": ConstantConfig(value=val.simplified_param),
        }
    )


def config_factory(config_type):
    @config_mapping
    def simplified_config(val: config_type) -> RunConfig:
        print(val)
        return get_run_conf_from_simplified_config(val)

    return simplified_config


@graph
def do_stuff_graph():
    add_one(return_constant())


do_stuff_simple1_job = do_stuff_graph.to_job(
    name="simple1", config=config_factory(SimplifiedConfig1)
)
do_stuff_simple2_job = do_stuff_graph.to_job(
    name="simple2", config=config_factory(SimplifiedConfig2)
)


@job(config=config_factory(SimplifiedConfig1))
def do_stuff_simple1():
    add_one(return_constant())


@job(config=config_factory(SimplifiedConfig2))
def do_stuff_simple2():
    add_one(return_constant())


@job
def do_stuff_plain():
    add_one(return_constant())


run_config = RunConfig(
    ops={"add_one": AddOneConfig(value=10), "return_constant": ConstantConfig(value=7)}
)


@job(config=run_config)
def do_stuff_with_config():
    add_one(return_constant())


def get_job_list() -> List[JobDefinition]:
    """returns a list of all niceml jobs"""
    return [
        do_stuff_simple1,
        do_stuff_simple2,
        do_stuff_plain,
        do_stuff_with_config,
        do_stuff_simple1_job,
        do_stuff_simple2_job,
    ]


@repository
def niceml_repository() -> List[JobDefinition]:
    """returns a list of all niceml jobs"""
    return get_job_list()
