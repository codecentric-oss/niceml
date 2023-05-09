"""Module for starting cli commands"""
import niceml
from invoke import Collection, Program

from niceml.cli import clicommands

program = Program(
    namespace=Collection.from_module(clicommands), version=niceml.__version__
)
