from niceml.config.hydra import InitConfig
from niceml.config.shared.models.confmodelscls import ConfModelCls
from niceml.config.trainparams import TrainParams
from niceml.dagster.ops.train import TrainConfig

CURRENT_EPOCHS = 1  # TODO: use function which extracts from environment?


class ConfDataDescriptionCls(InitConfig):
    """This class configures the data description for classification"""

    pass

class ConfOpTrainCls(TrainConfig):
    """This class configures the training op for classification"""

    train_params: TrainParams = TrainParams(epochs=CURRENT_EPOCHS)
    model_factory: InitConfig = ConfModelCls()
    data_description: InitConfig =
