"""Module for all Omegaconf utils """
import contextlib
from typing import Optional

from omegaconf import OmegaConf

from niceml.utilities.commonutils import str_to_bool


class StringSepResolver:  # pylint: disable=too-few-public-methods
    """
    OmegaConf resolver which extracts values from a string using the seperator

    Parameters:
        seperator: Used to split the input str
        cast_type: Optional; If given it is used to convert the value to a given type
    """

    def __init__(self, seperator: str = ",", cast_type=None):
        self.seperator = seperator
        self.cast_type = cast_type

    def __call__(self, incoming_str: str, index: int):
        """
        Extracts a value from 'incoming_str' by index
        Args:
            incoming_str: str with target information (e.g. '124,264')
            index: target index (e.g. 1 -> 264)
        """
        index = int(index)
        res = incoming_str.split(sep=self.seperator)[index]
        if self.cast_type is not None:
            res = self.cast_type(res)
        return res


class TypeCastResolver:  # pylint: disable=too-few-public-methods
    """Converts a string to a given type"""

    def __init__(self, cast_type):
        self.cast_type = cast_type

    def __call__(self, input_value: Optional[str]):
        return None if input_value is None else self.cast_type(input_value)


class TrueDivResolver:  # pylint: disable=too-few-public-methods
    """OmegaConf resolver which divides two values and returns an int"""

    def __call__(self, numerator: int, denominator: int):
        return int(float(numerator) // float(denominator))


def register_niceml_resolvers():
    """register all niceml OmegaConf resolvers"""
    # If this function is called twice, the Resolvers are already registered.
    # In this case, the upcoming ValueError is ignored.
    with contextlib.suppress(ValueError):
        OmegaConf.register_new_resolver(
            "niceml.extract_int", StringSepResolver(cast_type=int)
        )
        OmegaConf.register_new_resolver(
            "niceml.extract_float", StringSepResolver(cast_type=float)
        )
        OmegaConf.register_new_resolver("niceml.extract_raw", StringSepResolver())
        OmegaConf.register_new_resolver("niceml.to_int", TypeCastResolver(int))
        OmegaConf.register_new_resolver("niceml.to_float", TypeCastResolver(float))
        OmegaConf.register_new_resolver("niceml.to_bool", TypeCastResolver(str_to_bool))
        OmegaConf.register_new_resolver("niceml.true_div", TrueDivResolver())
