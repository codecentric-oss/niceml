"""Module for all experiment errors"""


class ModelNotFoundError(Exception):
    """Error when experiment has no model"""


class MetricNotAvailableError(Exception):
    """Error when a metric is not available"""


class LogEmptyError(Exception):
    """Error when the train logs are empty"""


class InfoNotFoundError(Exception):
    """Error when the experiment info is not found"""


class EmptyExperimentError(Exception):
    """Error when the experiment is empty"""


class ExperimentNotFoundError(Exception):
    """Error when the path doesn't contain an experiment"""


class AmbigousFilenameError(Exception):
    """Filename can be interpreted in multiple ways"""
