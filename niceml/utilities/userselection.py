"""Module for user selection dashboard component"""

from typing import List, Optional

import streamlit as st

from niceml.utilities.filtering.probabilityclassselector import Selection, SelectionInfo


# pylint: disable = too-many-arguments
def get_user_selection(
    selection_info: SelectionInfo,
    component_key: Optional[str] = None,
    class_label: str = "Class",
    prob_label: str = "Probability",
    data_identifier_options: Optional[List[str]] = None,
    data_identifier_label: str = "Data identifier",
    data_identifier_hint: Optional[str] = None,
) -> Selection:
    """
    Returns the users dashboard selection for specific values from a SelectionInfo.
    It creates the UI elements for selecting a class and probability value. It also
    allows users to select data points by their identifier (e.g., text).

    Args:
        selection_info: Information about the classes, min/max probability values and
            identifiers in the dataset
        component_key: Key to uniquely identify and update the component
        class_label: Label of the select box
        prob_label: Label for the probability slider
        data_identifier_options: List of data identifiers
        data_identifier_label: Label of the data identifier input
        data_identifier_hint: Hint provided to the user for selection of 'data_identifier_options'

    Returns:
        Selection object with user selection
    """
    container = st.container()
    sel_identifiers: Optional[List[str]] = None
    if data_identifier_options is not None and len(data_identifier_options) > 0:
        col_1, col_2, col_3 = container.columns(spec=3)
        sel_identifiers = col_3.multiselect(
            label=data_identifier_label,
            help=data_identifier_hint or "ID to select a specific data point",
            key=f"{component_key}_text_input",
            options=data_identifier_options or [],
        )
        sel_class = col_1.selectbox(
            label=class_label,
            options=selection_info.class_set,
            key=f"{component_key}_select_box",
        )
        col_2.markdown(
            "<div style='display: flex;align-items: center; justify-content:center; "
            "height:72px; width:100%;'>or</div>",
            unsafe_allow_html=True,
        )
    else:
        sel_class = container.selectbox(
            class_label,
            selection_info.class_set,
            key=f"{component_key}_select_box",
        )

    prob_val = st.slider(
        prob_label,
        selection_info.min_prob_value,
        selection_info.max_prob_value,
        selection_info.min_prob_value,
        key=f"{component_key}_slider",
    )
    return Selection(
        class_name=sel_class, prob_value=prob_val, identifiers=sel_identifiers or []
    )
