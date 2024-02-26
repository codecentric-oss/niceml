"""Module for CallbackInitializer"""
from typing import Dict, List, Optional

from dagster import Config
from pydantic import Field

from niceml.config.config import Configurable, InitConfig
from niceml.dlframeworks.keras.callbacks.callback_factories import CallbackFactory
from niceml.experiments.experimentcontext import ExperimentContext


class CallbackInitializer(Configurable):  # pylint: disable=too-few-public-methods
    """Initializes callbacks with ExperimentContext"""

    def __init__(
        self,
        callback_list: List[CallbackFactory],
        callback_dict: Dict[str, CallbackFactory],
    ):
        """
        Initializes callbacks with ExperimentContext
        Args:
            callback_list: A list of callback factories
            callback_dict: A dict of callback factories
        """
        super().__init__()
        self.callback_dict = callback_dict
        self.callback_list = callback_list

    def __call__(self, exp_context: ExperimentContext) -> List:
        """Initializes the callbacks"""
        callback_list = self.callback_list + list(self.callback_dict.values())
        cb_init_list = [cur_cb.create_callback(exp_context) for cur_cb in callback_list]
        return cb_init_list
