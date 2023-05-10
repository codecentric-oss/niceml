"""Module for clicommands provided with the package"""
import os
from os.path import join

import copier
import toml
from dotenv import load_dotenv
from invoke import task


load_dotenv(".env")


@task
def dagit(context):
    """Starts dagit with the niceml repository"""
    context.run("python -m dagit -m niceml.dagster.jobs.repository")


@task(help={"config_path": "config_path to your dashboard configuration"})
def dashboard(context, config_path="configs/dashboard/local.yaml"):
    """Starts the experiment dashboard"""
    import niceml.dashboard.dashboard as db_module  # pylint: disable=import-outside-toplevel

    run_file = db_module.__file__
    context.run(f"streamlit run {run_file} {config_path}")


@task(help={"config_path": "config_path to your job_train job config"})
def train(context, config_path):
    """Starts a job_train job"""
    execute_job(context, "job_train", config_path)


@task(help={"config_path": "config_path to your job_eval job config"})
def evaluation(context, config_path):
    """Starts a job_eval job"""
    execute_job(context, "job_eval", config_path)


@task(help={"config_path": "config_path to your job_data_generation job config"})
def gendata(
    context, config_path="configs/jobs/job_data_generation/job_data_generation.yaml"
):
    """Starts a job_data_generation job"""
    execute_job(context, "job_data_generation", config_path)


@task
def execute(context, job_name, config_path):
    """Starts a job with given name"""
    execute_job(context, job_name, config_path)


@task
def init(context):
    """Initializes an empty niceml project"""

    old_pyproject_toml = toml.load(
        join(os.path.abspath(os.getcwd()), "pyproject.toml")
    )["tool"]["poetry"]

    attributes_of_interest = [
        "name",
        "version",
        "description",
        "authors",
        "packages",
        "dependencies",
    ]
    copier_data_dict = {}

    for attribute in attributes_of_interest:
        try:
            attribute_value = old_pyproject_toml[attribute]
        except KeyError:
            continue
        copier_data_dict[attribute] = f"{attribute_value}"

        if attribute == "name":
            package_name = attribute_value.replace(" ", "")
            package_name = package_name.replace("-", "")
            package_name = package_name.replace("_", "")
            copier_data_dict["package_name"] = package_name

        if attribute == "authors":
            copier_data_dict[attribute] = attribute_value

        if attribute == "dependencies":
            copier_data_dict[attribute] = toml.dumps(
                attribute_value, encoder=toml.TomlPreserveInlineDictEncoder()
            )

    copier.run_auto(
        src_path="gh:codecentric-oss/niceml",
        dst_path=f"{os.path.abspath(os.getcwd())}",
        data=copier_data_dict,
        overwrite=True,
    )


def execute_job(context, job_name, config_path):
    """helper function to run jobs"""
    context.run(
        f"dagster job execute -m niceml.dagster.jobs.repository -j {job_name} -c {config_path}"
    )
