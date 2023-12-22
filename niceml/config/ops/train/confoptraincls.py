from niceml.config.trainparams import TrainParams
from niceml.dagster.ops.train import TrainConfig

CURRENT_EPOCHS = 1  # TODO: use function which extracts from environment?


class ConfOpTrainCls(TrainConfig):
    """This class configures the training op for classification"""

    train_params: TrainParams = TrainParams(epochs=CURRENT_EPOCHS)
