from dataclasses import dataclass
from typing import Any


@dataclass
class ModelBundle:
    model: Any
    optimizer: Any
    loss_func: Any
    metrics: list
