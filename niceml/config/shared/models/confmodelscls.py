"""This module contains the configuration class for classification models"""
from niceml.config.config import InitConfig
from niceml.dlframeworks.keras.models.mobilenet import OwnMobileNetModel


class ConfModelCls(InitConfig):
    """This class configures the model for classification"""

    target: str = InitConfig.create_target_field(OwnMobileNetModel)
    final_activation: str = "sigmoid"
