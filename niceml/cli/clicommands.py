"""Module for clicommands provided with the package"""
from dotenv import load_dotenv
from invoke import task

load_dotenv(".env")


@task
def dagit(context):
    """Starts dagit with the niceml repository"""
    context.run("python -m dagit -m niceml.dagster.jobs.repository")


@task(help={"config_path": "config_path to your dashboard configuration"})
def dashboard(context, config_path):
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
def gendata(context, config_path):
    """Starts a job_data_generation job"""
    execute_job(context, "job_data_generation", config_path)


@task
def execute(context, job_name, config_path):
    """Starts a job with given name"""
    execute_job(context, job_name, config_path)


def execute_job(context, job_name, config_path):
    """helper function to run jobs"""
    context.run(
        f"dagster job execute -m niceml.dagster.jobs.repository -j {job_name} -c {config_path}"
    )
