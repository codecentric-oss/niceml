"""Module to load hydra configurations"""
from os.path import abspath, basename, dirname
from typing import Dict, Optional

import click
from hydra import compose, initialize_config_dir
from omegaconf import OmegaConf


def load_hydra_conf(
    conf_path: str,
    additional_dict: Optional[Dict[str, str]] = None,
    remove_globals_after_resolving: bool = True,
) -> dict:
    """
    The load_hydra_conf function is a wrapper around the Hydra library.
    It loads a configuration file and returns it as a dictionary.
    The function also allows for additional parameters to be passed in,
     which will override any conflicting values in the config file.

    Args:
        conf_path: Specify the path to the configuration file
        additional_dict: Parameters which should be overwritten in the
            output dictionary
        remove_globals_after_resolving: Choose to remove globals from
            config after resolving the configuration. Removing is only
            applied if 'additional_dict' is given
    Returns
        A dictionary of loaded configurations
    """
    conf_dir = abspath(dirname(conf_path))
    config_file = basename(conf_path)
    with initialize_config_dir(config_dir=conf_dir, version_base="1.1"):
        cfg = compose(config_name=config_file)
        if additional_dict is not None:
            cfg = OmegaConf.to_container(cfg)
            globals_dict = {"globals": additional_dict}
            cfg = OmegaConf.merge(cfg, globals_dict)
            cfg = OmegaConf.to_container(cfg, resolve=True)
            if remove_globals_after_resolving:
                del cfg["globals"]
        else:
            OmegaConf.resolve(cfg)
            cfg = OmegaConf.to_container(cfg)
    return cfg


@click.command()
@click.argument("conf_path")
def load_hydra_conf_cmd(conf_path: str):
    """
    Command to load hydra configurations from file
    Args:
        conf_path: path to config file
    """
    load_hydra_conf(conf_path)


if __name__ == "__main__":
    load_hydra_conf_cmd()
