"""Module fot the abstract NetDataLogger"""

from abc import ABC, abstractmethod
from os.path import join
from typing import List

import numpy as np
from PIL import Image

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datainfos.datainfo import DataInfo
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import ExperimentFilenames


class NetDataLogger(ABC):
    """Abstract implementation of an NetDataLogger"""

    def __init__(self):
        self.data_description = None
        self.exp_context = None
        self.set_name = None
        self.output_path = None

    def initialize(
        self,
        data_description: DataDescription,
        exp_context: ExperimentContext,
        set_name: str,
    ):

        """Method to initialize the NetDataLogger"""
        self.data_description = data_description
        self.exp_context = exp_context
        self.set_name = set_name

    @abstractmethod
    def log_data(
        self,
        net_inputs: np.ndarray,
        net_targets: np.ndarray,
        data_info_list: List[DataInfo],
    ):
        """
        Logs the data sent as inputs and targets to a model,
        e.g. images and class labels or bounding boxes.

        Args:
            net_inputs: Input data of a model as `np.ndarray`
            net_targets: Target data of a model as `np.ndarray`
            data_info_list: Associated data information of input and
            destination with extended information

        Returns:
            None

        """

    def _save_img(self, image: Image.Image, filename: str):
        """
        Saves an `image`
        Args:
            image: image that will be saved
            filename: filename of the image

        """
        self.exp_context.write_image(
            image=image,
            data_path=join(ExperimentFilenames.NET_DATA_FOLDER, filename),
        )
