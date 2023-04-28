"""Module for keras callback to check Nan"""
from typing import List, Optional

import numpy as np
from tensorflow.python.keras.callbacks import (  # pylint: disable=no-name-in-module
    Callback,
)


class NanInLossError(Exception):
    """Error when loss is NaN"""


class LossNanCheckCallback(Callback):
    """Callback to check if nan is in loss"""

    def __init__(self, check_logs: Optional[List[str]] = None):
        super().__init__()
        self.check_logs = check_logs or ["loss", "val_loss"]

    def on_batch_end(self, batch, logs: Optional[dict] = None):
        if logs is None:
            return
        for cur_log in self.check_logs:
            if cur_log in logs:
                value = logs[cur_log]
                if value is None or np.isnan(value):
                    raise NanInLossError(
                        f"None in logs detected. batch: {batch}, logs: {logs}"
                    )
