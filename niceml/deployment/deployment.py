"""Module for the deployment cli function"""

import os
import shlex

from rich import print
import subprocess
import tempfile
from os.path import join
from typing import Optional

import typer
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from typing_extensions import Annotated

from niceml.experiments.expdatalocalstorageloader import create_expdata_from_expcontext
from niceml.experiments.experimentcontext import get_experiment_context
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.expfilenames import ExperimentFilenames, OpNames
from niceml.utilities.fsspec.locationutils import (
    open_location,
    join_fs_path,
    join_location_w_path,
)
from niceml.utilities.ioutils import (
    copy_file,
    read_txt,
    write_txt,
    read_yaml,
    write_yaml,
    list_dir,
)

load_dotenv(".env")

app = typer.Typer()


@app.command()
def serve(
    bundle_path: Annotated[Optional[str], typer.Option(help="Directory of the bundle ")] = "./"
):
    """
    The serve function is used to start a service that will serve the current bundle.

    Args:
        bundle_path: Path to the bundle
    """
    with open_location(join_location_w_path({"uri": bundle_path}, "bundle_info.yaml")) as (
        bundle_fs,
        bundle_info_path,
    ):
        bundle_info = read_yaml(filepath=bundle_info_path)
        service_module = bundle_info["service"]
        service_kwargs = bundle_info["service_kwargs"]

        print("[green]Start serving[/green] Current experiment will be available soon :rocket:")
        subprocess.run(
            shlex.split(
                f"python -m {service_module} "
                f"{' '.join(str(arg) for arg in service_kwargs.values())}"
            ),
            check=True,  # ruff: noqa: S603
            shell=False,
        )


# S104 is disabled here because the host default is only used for the creation of the Dockerfile
@app.command()
def bundle(  # ruff: noqa: PLR0913
    service_path: Annotated[str, typer.Option(help="Module path to the API service module")],
    exp_id: Annotated[
        Optional[str],
        typer.Option(help="Experiment ID of the experiment to be bundled"),
    ] = None,
    exp_location: Annotated[
        Optional[str], typer.Option(help="Path to the experiments folder")
    ] = None,
    extras: Annotated[
        str,
        typer.Option(help="Poetry extras to be included in the bundle requirements"),
    ] = None,
    python_version: Annotated[
        str, typer.Option(help="Python version that should be used for the bundle")
    ] = "3.10.0",
    port: Annotated[int, typer.Option(help="The port that the service will be exposed on")] = 8000,
    host: Annotated[
        str, typer.Option(help="Host IP address that the service will be running on")
    ] = "0.0.0.0",  # ruff: noqa: S104
):
    """
    The bundle function will create a folder called `bundle` in the experiment root directory.
    This folder contains all the necessary files for creating and deploying an image or
    serve a model as a service


    Args:
        service_path: Module path of the service to access the model
        exp_id: Experiment id of the experiment to bundle
        exp_location: Location of the experiments
        extras: Poetry extras to be included in the bundle requirements
        python_version: Python version that should be used for the bundle
        port:The port that the service will be exposed on
        host: Host IP address that the service will be running on
    """

    print(
        f"[green]Start bundling[/green]\t\tCreate bundle for "
        f"experiment [bold]{exp_id}[bold] :hammer:"
    )
    extras: str = extras or ""
    exp_location = eval(exp_location or os.getenv("EXPERIMENT_LOCATION"))
    experiment_context = get_experiment_context(exp_location=exp_location, exp_id=exp_id)
    exp_data: ExperimentData = create_expdata_from_expcontext(experiment_context)
    with open_location(experiment_context.fs_config) as (exp_fs, exp_root):
        with tempfile.TemporaryDirectory() as tmp_dir:
            print("[dark_orange]Bundling[/dark_orange]\t\tExport required environment dependencies")
            requirements_path = f"{tmp_dir}/requirements.txt"
            extras_string = [f"-E {extra}" for extra in extras.replace(" ", "").split(",")]
            subprocess.run(
                shlex.split(
                    f"poetry export -f requirements.txt --output {tmp_dir}/requirements.txt "
                    f"{' '.join(extras_string)} --without-hashes"
                ),
                shell=False,
                check=True,  # ruff: noqa: S603
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            requirements = read_txt(filepath=requirements_path)
            write_txt(
                content=requirements,
                filepath=join_fs_path(exp_fs, exp_root, "bundle", "env", "requirements.txt"),
                file_system=exp_fs,
            )
        print("[dark_orange]Bundling[/dark_orange]\t\tCreate project wheel")
        subprocess.run(
            shlex.split("poetry build -f wheel"),
            shell=False,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        copy_file(
            source="./dist/*.whl",
            destination=join_fs_path(exp_fs, exp_root, "bundle"),
            file_system=exp_fs,
        )
        wheels = list_dir(
            path=join_fs_path(exp_fs, exp_root, "bundle"),
            filter_ext=[".whl"],
            file_system=exp_fs,
        )
        wheel_name = wheels[0]

        print("[dark_orange]Bundling[/dark_orange]\t\tCopy files")

        copy_file(
            source="./pyproject.toml",
            destination=join_fs_path(exp_fs, exp_root, "bundle", "env", "python", "pyproject.toml"),
            file_system=exp_fs,
        )
        copy_file(
            source="./poetry.lock",
            destination=join_fs_path(exp_fs, exp_root, "bundle", "env", "python", "poetry.lock"),
            file_system=exp_fs,
        )
        print("[dark_orange]Bundling[/dark_orange]\t\tCreate bundle info")

        model_custom_objects = read_yaml(
            filepath=join(
                exp_root,
                ExperimentFilenames.CONFIGS_FOLDER,
                OpNames.OP_TRAIN.value,
                ExperimentFilenames.CUSTOM_LOAD_OBJECTS,
            ),
        )
        model_loader = read_yaml(
            filepath=join(
                exp_root,
                ExperimentFilenames.CONFIGS_FOLDER,
                OpNames.OP_PREDICTION.value,
                ExperimentFilenames.MODEL_LOADER,
            ),
        )
        data_description_path = join(
            ExperimentFilenames.CONFIGS_FOLDER,
            OpNames.OP_TRAIN.value,
            ExperimentFilenames.DATA_DESCRIPTION,
        )

        model_path = exp_data.get_model_path()
        working_directory = ".."
        config_dict = {
            "working_directory": working_directory,
            "assets": {
                "exp_info": {
                    "loader": {"_target_": "niceml.utilities.ioutils.load_yaml_factory"},
                    "path": ExperimentFilenames.EXP_INFO,
                    "kwargs": {},
                },
                "data_description": {
                    "loader": {"_target_": "niceml.config.hydra.instantiate_from_yaml_factory"},
                    "path": data_description_path,
                    "kwargs": {},
                },
                "model": {
                    "loader": model_loader,
                    "path": model_path,
                    "kwargs": model_custom_objects,
                },
            },
            "service": service_path,
            "service_kwargs": {
                "host": host,
                "port": port,
            },
        }
        write_yaml(
            data=config_dict,
            filepath=join_fs_path(exp_fs, exp_root, "bundle", "bundle_info.yaml"),
            file_system=exp_fs,
        )

        print("[dark_orange]Bundling[/dark_orange]\t\tWrite Dockerfile")

        template_env = Environment(
            loader=FileSystemLoader(f"{os.getcwd()}/niceml/utilities/assets/templates/docker"),
            autoescape=True,
        )

        docker_template = template_env.get_template("Dockerfile_exp.jinja")
        rendered_dockerfile = docker_template.render(
            python_version=python_version,
            data_description_path=data_description_path,
            exp_info_path=ExperimentFilenames.EXP_INFO,
            model_path=model_path,
            entry_point=f'["python","-m","{service_path}", "{host}", "{port}"]',
            wheel_name=wheel_name,
            port=port,
            working_directory=working_directory,
        )

        write_txt(
            content=rendered_dockerfile,
            filepath=join_fs_path(exp_fs, exp_root, "bundle", "env", "docker", "Dockerfile"),
            file_system=exp_fs,
        )

        write_txt(
            content=python_version,
            filepath=join_fs_path(exp_fs, exp_root, "bundle", "env", "version.txt"),
            file_system=exp_fs,
        )
        print(
            f"[green]Finished bundling[/green]\tBundle for experiment "
            f"[bold]{exp_id}[/bold] created :white_check_mark:"
        )


if __name__ == "__main__":
    app()
