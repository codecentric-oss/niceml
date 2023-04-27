"""Module for data tests"""
import click
import yaml


def run_datatests(config_file: str, data_folder: str):
    """
    Run data tests

    Args:
        config_file: path to file with data test configuration
        data_folder: data to test
    """
    with open(config_file, "r") as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    test_process = config["tests"]
    test_process(data_folder, data_folder)


@click.command()
@click.argument("config_file")
@click.argument("data_folder")
def run_datatests_cmd(config_file: str, data_folder: str):
    """Command to run data tests"""
    run_datatests(config_file, data_folder)


if __name__ == "__main__":
    run_datatests_cmd()  # pylint: disable=no-value-for-parameter
