"""ModelCheckpoint that supports fsspec filesystems."""
import logging
from os.path import dirname, join
from tempfile import TemporaryDirectory
from typing import Optional, Union

from fsspec import AbstractFileSystem
from keras.callbacks import ModelCheckpoint as ModelCheckpointKeras
from keras.utils import io_utils, tf_utils

from niceml.utilities.fsspec.locationutils import LocationConfig, open_location


class ModelCheckpoint(ModelCheckpointKeras):
    """ModelCheckpoint that supports fsspec filesystems.
    Subclassed and adapted from https://github.com/keras-team/keras/blob/master/keras/callbacks.py
    """

    def __init__(
        self,
        output_location: Union[dict, LocationConfig],
        file_formats: Optional[dict] = None,
        **kwargs,
    ):
        super().__init__("", **kwargs)
        self.output_location = output_location
        self.file_formats = file_formats or {}

    def _should_save(self, epoch, logs) -> bool:
        """Determines whether the model should be saved."""
        if self.save_best_only:
            current = logs.get(self.monitor)
            if current is None:
                raise ValueError(
                    "Can save best model only with %s available, "
                    "got %s." % (self.monitor, list(logs.keys()))
                )
            else:
                if self.monitor_op(current, self.best):
                    if self.verbose > 0:
                        io_utils.print_msg(
                            f"\nEpoch {epoch + 1}: {self.monitor} improved "
                            f"from {self.best:.5f} to {current:.5f}"
                        )
                    self.best = current
                    return True
                if self.verbose > 0:
                    io_utils.print_msg(
                        f"\nEpoch {epoch + 1}: "
                        f"{self.monitor} did not improve from {self.best:.5f}"
                    )
        else:
            if self.verbose > 0:
                io_utils.print_msg(f"\nEpoch {epoch + 1}: saving model")
            return True
        return False

    def _save_model(self, epoch, batch, logs):
        """Saves the model.

        Args:
            epoch: the epoch this iteration is in.
            batch: the batch this iteration is in. `None` if the `save_freq`
              is set to `epoch`.
            logs: the `logs` dict passed in to `on_batch_end` or `on_epoch_end`.
        """
        logs = logs or {}

        if (
            isinstance(self.save_freq, int)
            or self.epochs_since_last_save >= self.period
        ):
            # Block only when saving interval is reached.
            logs = tf_utils.sync_to_numpy_or_python_type(logs)
            self.epochs_since_last_save = 0
            if self._should_save(epoch, logs):
                target_fs: AbstractFileSystem
                with open_location(self.output_location) as (target_fs, target_path):
                    target_fs.makedirs(dirname(target_path), exist_ok=True)
                    target_path = target_path.format(
                        epoch=epoch + 1, **self.file_formats, **logs
                    )
                    with target_fs.open(
                        target_path, "wb"
                    ) as model_file, TemporaryDirectory() as temp_dir:
                        tmp_path = join(temp_dir, "model.h5")
                        if self.save_weights_only:
                            self.model.save_weights(
                                tmp_path,
                                overwrite=True,
                                options=self._options,
                                save_format="h5",
                            )
                        else:
                            self.model.save(
                                tmp_path,
                                overwrite=True,
                                options=self._options,
                                save_format="h5",
                            )
                        with open(tmp_path, "rb") as tmp_model_file:
                            model_file.write(tmp_model_file.read())
                        logging.info("Saved model to %s", target_path)
