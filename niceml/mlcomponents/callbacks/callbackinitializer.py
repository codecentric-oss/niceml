"""Module for CallbackInitializer"""
from typing import Dict, List, Optional

from dagster import Config
from pydantic import Field

from niceml.dlframeworks.keras.callbacks.callback_factories import CallbackFactory
from niceml.experiments.experimentcontext import ExperimentContext


class CallbackInitializer(Config):  # pylint: disable=too-few-public-methods
    """Initializes callbacks with ExperimentContext"""

    callback_list: List[CallbackFactory] = Field(
        default_factory=list, description="A list of callback factories"
    )
    callback_dict: Dict[str, CallbackFactory] = Field(
        default_factory=dict, description="A dict of callback factories"
    )

    def __call__(self, exp_context: ExperimentContext) -> List:
        """Initializes the callbacks"""
        callback_list = self.callback_list + list(self.callback_dict.values())
        cb_init_list = [cur_cb.create_callback(exp_context) for cur_cb in callback_list]
        return cb_init_list
