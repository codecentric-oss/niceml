"""Module for the image netdata logger visualization components"""

from os.path import basename
from typing import List, Optional

import numpy as np
import streamlit as st

from niceml.dashboard.netdataloggerviscomponent import NetDataLoggerVisComponent
from niceml.data.dataloaders.interfaces.imageloader import ImageLoader
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentmanager import ExperimentManager
from niceml.experiments.expfilenames import ExperimentFilenames


class ImageNetDataLoggerVisComponent(NetDataLoggerVisComponent):
    """Dashboard component to visualize the net data of an experiment (currently images)"""

    def __init__(
        self,
        image_loader: ImageLoader,
        column_amount: int = 1,
        max_output_count: int = 10,
        **kwargs,
    ):
        """
        Dashboard component to visualize the net data of an experiment (currently images)

        Args:
            image_loader: Image loader to load the net data images
            column_amount: Amount of columns that are used to visualize the images
            max_output_count: Max number of net data to be displayed
            **kwargs:
        """
        super().__init__(**kwargs)
        self.max_output = max_output_count
        self.column_amount = column_amount
        self.image_loader: ImageLoader = image_loader

    def _render(
        self,
        exp_manager: ExperimentManager,
        storage_interface: StorageInterface,
        exp_id: str,
        subset_name: Optional[str] = None,
    ):
        exp: ExperimentData = exp_manager.get_exp_by_id(exp_id)
        net_data_paths = exp.get_file_paths(ExperimentFilenames.NET_DATA_FOLDER, ".png")
        net_data_paths.sort()
        if len(net_data_paths) == 0:
            st.info("No data was logged for this experiment.")
            return

        @st.cache_data()
        def _load_net_data(
            *args,  # pylint: disable = unused-argument
        ) -> List[np.ndarray]:

            return [
                self.image_loader(filepath=net_data_path)
                for net_data_path in net_data_paths[: self.max_output]
            ]

        images = _load_net_data(exp_id, subset_name)
        columns = st.columns(self.column_amount)
        for idx, image in enumerate(images):
            col = columns[idx % self.column_amount]
            col.image(
                image, caption=self._get_image_caption(exp_data=exp, net_data_idx=idx)
            )

    @staticmethod
    def _get_image_caption(exp_data: ExperimentData, net_data_idx: int) -> str:
        """
        Returns a caption for a net data image

        Args:
            exp_data: experiment data
            net_data_idx: index of the netdata for which the caption is to be created

        Returns:
            Caption string

        """
        net_data_paths = exp_data.get_file_paths(
            ExperimentFilenames.NET_DATA_FOLDER, ".png"
        )
        net_data_paths.sort()
        return basename(net_data_paths[net_data_idx])
