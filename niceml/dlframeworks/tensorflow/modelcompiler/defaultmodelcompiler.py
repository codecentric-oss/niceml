"""Module for model compilers in tensorflow"""
from typing import Any, List, Union

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.mlcomponents.modelcompiler.modelcompiler import ModelCompiler
from niceml.mlcomponents.models.modelbundle import ModelBundle
from niceml.mlcomponents.models.modelfactory import ModelFactory


class DefaultModelCompiler(ModelCompiler):  # pylint: disable=too-few-public-methods
    """Simplest model compiler for tensorflow"""

    def __init__(
        self, loss: Union[str, dict], metrics: List, optimizer: dict, **kwargs
    ):
        self.loss = loss
        self.metrics = metrics
        self.optimizer = optimizer
        self.compiler_args: dict = kwargs

    def compile(
        self, model_factory: ModelFactory, data_description: DataDescription
    ) -> ModelBundle:
        model = model_factory.create_model(data_description)
        model.compile(
            optimizer=self.optimizer,
            loss=self.loss,
            metrics=self.metrics,
            **self.compiler_args,
        )
        return ModelBundle(model, self.optimizer, self.loss, self.metrics)


class ComplexModelCompiler(ModelCompiler):  # pylint: disable=too-few-public-methods
    """Complex model compiler for tensorflow"""

    def __init__(
        self,
        optimizer: Union[dict, Any],
        metrics: List,
        losses: dict = None,
    ):
        self.losses = losses
        self.optimizer = optimizer
        self.metrics = metrics

    def compile(self, model_factory: ModelFactory, data_description: DataDescription):
        target_loss = {}
        loss_weights = {}
        for loss_name, loss_info in self.losses.items():
            target_loss[loss_name] = loss_info["target"]
            loss_weights[loss_name] = loss_info["weight"]

        model = model_factory.create_model(data_description)
        model.compile(
            optimizer=self.optimizer,
            loss=target_loss,
            metrics=self.metrics,
            loss_weights=loss_weights,
        )
        return ModelBundle(model, self.optimizer, target_loss, self.metrics)
