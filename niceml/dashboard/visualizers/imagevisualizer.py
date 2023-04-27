"""Module for ImageVisualizer"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from os.path import basename
from typing import List, Type, Union

import numpy as np
import pandas as pd
import streamlit as st

from niceml.data.dataloaders.interfaces.imageloader import ImageLoader
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.instancelabeling import InstanceLabel


@dataclass
class ImageContainer:
    """Collection of one or more images, the corresponding prediction and ground truth
    `InstanceLabel`s and the underlying data of the `InstanceLabel`s."""

    image_path: Union[str, List[str]]
    predictions: List[InstanceLabel]
    ground_truth: List[InstanceLabel]
    visualize_data: pd.DataFrame
    model_output_size: ImageSize
    image_visu_size: ImageSize

    def get_image_paths(self) -> List[str]:
        """
        Returns image path(s) as list

        Returns:
            List of image paths
        """
        if isinstance(self.image_path, list):
            return self.image_path
        return [self.image_path]

    def scale_instance_labels(self, scale_factor: float) -> "ImageContainer":
        """
        Scales the images prediction and ground truth instance labels with a given
        `scale_factor` and returns a new scaled instance of `ImageContainer`

        Args:
            scale_factor: Factor to scale the prediction and ground truth labels by

        Returns:
            Scaled ImageContainer
        """

        scaled_predictions = [
            prediction.scale_label(scale_factor) for prediction in self.predictions
        ]
        scaled_ground_truth = [
            ground_truth.scale_label(scale_factor) for ground_truth in self.ground_truth
        ]

        return ImageContainer(
            image_path=self.image_path,
            predictions=scaled_predictions,
            ground_truth=scaled_ground_truth,
            visualize_data=self.visualize_data,
            image_visu_size=self.image_visu_size,
            model_output_size=self.model_output_size,
        )


class ImageVisualizer(ABC):  # pylint: disable = too-few-public-methods
    """Visualizer for images of `ImageContainer`s"""

    def __init__(
        self,
        image_loader: ImageLoader,
        columns_count: int = 2,
    ):
        self.columns_count = columns_count
        self.image_loader = image_loader

    def visualize_images(  # pylint: disable = too-many-arguments
        self,
        image_data_containers: List[ImageContainer],
    ):
        """
        Visualizes images from 'image_data_containers' with prediction and ground truth
        labels in streamlit container

        Args:
            image_data_containers: ImageContainer storing information about the images
                and labels to visualize
        """

        for image_data_container in image_data_containers:
            image_data_list = self.get_images_with_labels(image_data_container)
            dashboard_container = st.container()

            columns = dashboard_container.columns(self.columns_count)

            for idx, (image, path) in enumerate(
                zip(image_data_list, image_data_container.get_image_paths())
            ):
                columns[idx % self.columns_count].image(image, caption=basename(path))

            if image_data_container.visualize_data.empty:
                dashboard_container.caption("No predictions found")
            elif len(image_data_list) == 0:
                # pylint:disable = line-too-long
                st.warning(
                    f"File not found ({', '.join([basename(path)for path in image_data_container.get_image_paths()])}"
                )
            else:
                dashboard_container.dataframe(image_data_container.visualize_data)

    @abstractmethod
    def get_images_with_labels(
        self, image_data_container: ImageContainer
    ) -> List[np.ndarray]:
        """Returns images of 'image_data_container' with drawn prediction and ground truth labels"""


def check_instance_label_type(
    label_list: List[InstanceLabel], target_type: Type[InstanceLabel]
) -> bool:
    """
    Check if each label in `label_list` is an instance of `target_type`

    Args:
        label_list: List of labels for which the type is to be checked
        target_type: Type to be checked

    Returns:
        True if each label of `label_list` is an instance of `target_type`,
        otherwise False.
    """

    return all(isinstance(label, target_type) for label in label_list)
