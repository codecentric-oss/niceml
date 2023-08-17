import os
import shutil
import subprocess
from typing import Optional
import typer

app = typer.Typer()


@app.command()
def build(
    model_file: str,
    fastapi_module: str,
    bundle_location: Optional[str] = ".",
    extras: Optional[str] = None,
):
    # Generate wheel with poetry
    subprocess.run(["poetry", "build"])

    # Copy model file
    shutil.copy(model_file, bundle_location)

    # Copy pyproject.toml and poetry.lock
    shutil.copy("pyproject.toml", bundle_location)
    shutil.copy("poetry.lock", bundle_location)

    # Copy the generated wheel to bundle location
    wheel_file = get_generated_wheel()
    shutil.copy(wheel_file, os.path.join(bundle_location, os.path.basename(wheel_file)))

    # Generate Dockerfile
    generate_dockerfile(fastapi_module, bundle_location, extras)

    typer.echo(f"Bundle generated at {bundle_location}")


def get_generated_wheel() -> str:
    # Get the location of the generated wheel file
    build_dir = "dist"
    wheel_files = [f for f in os.listdir(build_dir) if f.endswith(".whl")]
    return os.path.join(build_dir, wheel_files[0])


def generate_dockerfile(
    fastapi_module: str, bundle_location: str, extras: Optional[str]
):
    # Read Dockerfile template
    with open("Dockerfile.jinja", "r") as f:
        template = f.read()

    # Substitute placeholder with extras
    if extras:
        template = template.replace("{EXTRAS}", extras)
    else:
        template = template.replace("{EXTRAS}", "")

    # Generate Dockerfile
    with open(os.path.join(bundle_location, "Dockerfile"), "w") as f:
        f.write(template.replace("{FASTAPI_MODULE}", fastapi_module))


@app.command()
def containerize(bundle_location: str):
    subprocess.run(["docker", "build", "-t", "ml_bundle", bundle_location])


@app.command()
def serve(fastapi_module: str):
    subprocess.run(
        ["uvicorn", f"{fastapi_module}:app", "--host", "0.0.0.0", "--port", "8000"]
    )


if __name__ == "__main__":
    app()
