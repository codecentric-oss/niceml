"""Module for starting cli commands"""
import pkg_resources
from invoke import Collection, Program

from niceml.cli import clicommands

my_version = pkg_resources.get_distribution("niceml").version
program = Program(namespace=Collection.from_module(clicommands), version=my_version)
