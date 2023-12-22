from typing import List

from keras.optimizers import Adam

from niceml.config.hydra import InitConfig, MapInitConfig, get_class_path
from niceml.config.shared.confdatasets import (
    ConfDatasetClsTrain,
    ConfDatasetClsValidation,
)
from niceml.config.shared.confexpoutinitializer import ConfDefaultExpOutInitializer
from niceml.config.shared.models.confmodelscls import ConfModelCls
from niceml.config.trainparams import TrainParams
from niceml.dagster.ops.train import TrainConfig
from niceml.data.datadescriptions.clsdatadescription import ClsDataDescription
from niceml.dlframeworks.keras.callbacks.callback_factories import (
    LoggingOutputCallbackFactory,
    InitCallbackFactory,
    ModelCallbackFactory,
)
from niceml.dlframeworks.keras.callbacks.nancheckcallback import LossNanCheckCallback
from niceml.dlframeworks.keras.learners.keraslearner import KerasLearner
from niceml.dlframeworks.keras.modelcompiler.defaultmodelcompiler import (
    DefaultModelCompiler,
)
from niceml.mlcomponents.callbacks.callbackinitializer import CallbackInitializer
from niceml.mlcomponents.modelcompiler.modelcustomloadobjects import (
    ModelCustomLoadObjects,
)
from niceml.utilities.imagesize import ImageSize

CURRENT_EPOCHS = 1  # TODO: use function which extracts from environment?


class ConfOptimizerCls(InitConfig):
    """This class configures the optimizer for classification"""

    target: str = InitConfig.create_target_field(Adam)
    learning_rate: float = 0.0001


class ConfDefaultModelCompiler(InitConfig):
    """This class configures the default model compiler for classification"""

    target: str = InitConfig.create_target_field(DefaultModelCompiler)
    optimizer: InitConfig = ConfOptimizerCls()
    loss: str = "binary_crossentropy"
    metrics: List[str] = ["accuracy"]


class ConfCheckLossNanCallback(InitConfig):
    """This class configures the check loss nan callback for classification"""

    target: str = InitConfig.create_target_field(InitCallbackFactory)
    callback: InitConfig = InitConfig.create_config(LossNanCheckCallback)


class ConfSaveModelCallback(InitConfig):
    """This class configures the save model callback for classification"""

    target: str = InitConfig.create_target_field(ModelCallbackFactory)
    model_subfolder: str = "models/model-id_{short_id}-ep{epoch:03d}.hdf5"


class ConfCallbackDict(MapInitConfig):
    """This class configures the callback dict for classification"""

    logging_output: InitConfig = InitConfig.create_config(LoggingOutputCallbackFactory)
    check_loss_nan: InitConfig = ConfCheckLossNanCallback()
    save_model: InitConfig = ConfSaveModelCallback()


class ConfCallbackInitializer(InitConfig):
    """This class configures the callback initializer for classification"""

    target: str = InitConfig.create_target_field(CallbackInitializer)
    callback_dict: MapInitConfig = ConfCallbackDict()


class ConfClsKerasLearner(InitConfig):
    """This class configures the learner for classification"""

    target: str = InitConfig.create_target_field(KerasLearner)
    model_compiler: InitConfig = ConfDefaultModelCompiler()
    model_load_custom_objects: InitConfig = InitConfig.create_config(
        ModelCustomLoadObjects
    )


model_compiler = InitConfig.create(
    DefaultModelCompiler,
    optimizer=ConfOptimizerCls(),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)

keras_learner = InitConfig.create(
    KerasLearner,
    model_compiler=dict(
        _target_=get_class_path(DefaultModelCompiler),
        optimizer=ConfOptimizerCls(),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    ),
    model_load_custom_objects=dict(_target_=get_class_path(ModelCustomLoadObjects)),
)


class ConfDataDescriptionCls(InitConfig):
    """This class configures the data description for classification"""

    target: str = InitConfig.create_target_field(ClsDataDescription)
    classes: List[str] = ["0", "1"]
    use_binary: bool = True
    target_size: ImageSize = ImageSize(width=64, height=64)


class ConfOpTrainCls(TrainConfig):
    """This class configures the training op for classification"""

    train_params: TrainParams = TrainParams(epochs=CURRENT_EPOCHS)
    model_factory: InitConfig = ConfModelCls(final_activation="softmax")
    data_description: InitConfig = ConfDataDescriptionCls()
    data_train: InitConfig = ConfDatasetClsTrain()
    data_validation: InitConfig = ConfDatasetClsValidation()
    learner: InitConfig = ConfClsKerasLearner()
    # TODO: exp_initializer should be located differently
    exp_initializer: InitConfig = ConfDefaultExpOutInitializer()
