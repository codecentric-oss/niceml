from typing import List

from niceml.config.hydra import InitConfig
from niceml.experiments.expoutinitializer import ExpOutInitializer


class ConfDefaultExpOutInitializer(InitConfig):
    """Config for ExpOutInitializer"""

    target: str = InitConfig.create_target_field(ExpOutInitializer)
    exp_name: str = "Classification Experiment"
    exp_prefix: str = "CLS"
    git_modules: List[str] = ["niceml"]
