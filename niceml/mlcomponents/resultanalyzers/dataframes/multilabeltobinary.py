from typing import List, Union

import numpy as np
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

from niceml.experiments.experimentcontext import ExperimentContext
from niceml.mlcomponents.resultanalyzers.dataframes.clsmetric import cl_metric_dict
from niceml.mlcomponents.resultanalyzers.dataframes.dfanalyzer import DfMetric


class MultilabelBinaryMetric(DfMetric):
    def __init__(
        self,
        source_col: str,
        target_cols_prefix: str,
        positive_indexes: List[int],
        lower_thres: float = 0.5,
        function: Union[str, dict] = "accuracy",
        name_suffix: str = "",
    ):
        """
        Converts a multilabel classification problem to a binary.
        Uses the `positive_indexes` class as positive class.
        If any of these class indexes is higher than `threshold`
        it is counted as positive class and negative otherwise.

        Parameters
        ----------
        source_col: str
            name of the column with the class index or indexes (multitarget)
        target_cols_prefix: str
            starting name of the columns containing the output of the model
        positive_indexes: List[int]
            indexes of the positive classes.
            Has to be match with the index in `classes` in the
            datasets.yml -> data_description
        lower_thres: float, default 0.5
            lower threshold for the positive classes to be counted as true
        function: str or dict, default "accuracy"
            function to calculate the metric.
            If str is given it must be a key of the `cl_metric_dict`.
            Otherwise the given dict is initialized with `init_object`
            and additional the key `name`
            must be available to define the output
            name in the result dict.
        name_suffix: str, default ""
            can be used to add a str to the dict output name
            (e.g. if the same metric should be applied
            to multiple columns)
        """
        self.source_col = source_col
        self.target_cols_prefix = target_cols_prefix
        self.name_suffix = name_suffix
        self.positive_indexes = positive_indexes
        self.lower_thres = lower_thres
        if type(function) is str:
            self.func_name = function
            try:
                self.function = cl_metric_dict[function]
            except KeyError as e:
                raise Exception(
                    f"Function with name {function} not supported!"
                    f" Available: {list(cl_metric_dict.keys())}"
                ) from e
        else:
            self.func_name = function["name"]
            self.function = function["target"]

    def __call__(
        self,
        data: pd.DataFrame,
        exp_context: ExperimentContext,
        dataset_name: str,
        **kwargs,
    ) -> dict:
        target_cols = [x for x in data.columns if x.startswith(self.target_cols_prefix)]
        array = data[target_cols].to_numpy()
        positive_pred_array = array[:, self.positive_indexes]
        positive_pred_array = positive_pred_array > self.lower_thres
        positive_pred_array = np.any(positive_pred_array, axis=1).astype(float)

        label_binarizer = MultiLabelBinarizer(classes=list(range(len(target_cols))))
        binarized_labels = label_binarizer.fit_transform(data[self.source_col])
        positive_labels = binarized_labels[:, self.positive_indexes].astype(bool)
        positive_labels = np.any(positive_labels, axis=1).astype(float)
        value = self.function(positive_labels, positive_pred_array)
        if isinstance(value, np.ndarray):
            value = value.tolist()
        else:
            value = float(value)
        return {f"{self.func_name}{self.name_suffix}": value}
