"""Implementation of the CSVLogger callback for TensorFlow."""
import numpy as np
import pandas as pd
from keras.callbacks import Callback

from niceml.experiments.experimentcontext import ExperimentContext


class CSVLogger(Callback):
    """Callback that streams epoch results to a CSV file.

    Supports all values that can be represented as a string,
    including 1D iterables such as np.ndarray.

    # Example
    ```python
    csv_logger = CSVLogger(exp_context=exp_context)
    model.fit(X_train, Y_train, callbacks=[csv_logger])
    ```

    # Arguments
        exp_context: An instance of ExperimentContext which is used to write csv files
        separator: string used to separate elements in the CSV file.
    """

    def __init__(
        self, experiment_context: ExperimentContext, filename: str = "train_logs.csv"
    ):
        self.filename = filename
        self.keys = None
        self.data = None
        self.experiment_context = experiment_context
        super().__init__()

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}

        if self.keys is None:
            self.keys = sorted(logs.keys())

        if self.data is None:
            self.data = pd.DataFrame(columns=["epoch"] + self.keys)

        row_dict = {"epoch": epoch + 1}
        row_dict.update({k: np.round(v, 6) for k, v in logs.items()})
        self.data = self.data.append(row_dict, ignore_index=True)
        self.flush()

    def on_train_end(self, logs=None):
        self.flush()

    def flush(self):
        if self.experiment_context is not None:
            self.experiment_context.write_csv(self.data, data_path=self.filename)
