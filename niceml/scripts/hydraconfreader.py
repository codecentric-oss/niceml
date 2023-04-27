"""Module to load hydra configurations"""
from os.path import abspath, basename, dirname

import click
from hydra import compose, initialize_config_dir
from omegaconf import OmegaConf


def load_hydra_conf(conf_path: str) -> dict:
    """Load and instantiate instances which are configured in files of a directory"""
    conf_dir = abspath(dirname(conf_path))
    config_file = basename(conf_path)
    with initialize_config_dir(config_dir=conf_dir, version_base="1.1"):
        cfg = compose(config_name=config_file)
        OmegaConf.resolve(cfg)
        cfg = OmegaConf.to_container(cfg)
    return cfg


@click.command()
@click.argument("conf_path")
def load_hydra_conf_cmd(conf_path: str):
    """Command to load hydra configuration"""
    load_hydra_conf(conf_path)


if __name__ == "__main__":
    load_hydra_conf_cmd()  # pylint: disable=no-value-for-parameter
