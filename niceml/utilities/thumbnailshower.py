"""Module for ImageThumbnailShower"""
from typing import List, Optional, Union

import numpy as np
import streamlit as st
from PIL import Image


class ImageThumbnailShower:  # pylint: disable=too-few-public-methods
    """Class to show image thumbnails in a gridview in streamlit"""

    def __init__(self, col_count: int, selectable: bool = True):
        self.col_count = col_count
        self.selectable = selectable

    def show_thumbnails(
        self, image_list: List[Union[np.ndarray, Image.Image]], image_ids: List[str]
    ) -> Optional[int]:
        """Shows image thumbnails in a gridview component in streamlit

        Args:
            image_list: List of images to show
            image_ids: Ids of the images to show

        Returns:
            Index of image when an id is selected in the component
        """
        columns = st.columns(self.col_count)
        selection_idx: Optional[int] = None
        for idx, image in enumerate(image_list):
            cur_col = columns[idx % self.col_count]
            cur_id = image_ids[idx]
            caption = None if self.selectable else cur_id
            cur_col.image(image, use_column_width=True, caption=caption)
            if self.selectable and cur_col.button(cur_id):
                selection_idx = idx
        return selection_idx
