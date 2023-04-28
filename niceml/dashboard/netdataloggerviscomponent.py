"""Module for the net data logger visualization component"""
from abc import ABC

from niceml.dashboard.components.expviscomponent import SingleExpVisComponent


class NetDataLoggerVisComponent(SingleExpVisComponent, ABC):
    """Abstract class of a net data logger visualization component"""
