"""Module for clsmetric"""
from typing import Union

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
)
from sklearn.preprocessing import MultiLabelBinarizer

from niceml.experiments.experimentcontext import ExperimentContext
from niceml.mlcomponents.resultanalyzers.dataframes.dfanalyzer import DfMetric

cl_metric_dict = dict(
    accuracy=accuracy_score,
    confusion_matrix=confusion_matrix,
    f1_score=f1_score,
    precision=precision_score,
    recall=recall_score,
    precision_recall_curve=precision_recall_curve,
)


class ClsMetric(DfMetric):
    def __init__(
        self,
        source_col: str,
        target_cols_prefix: str,
        function: Union[str, dict] = "accuracy",
        name_suffix: str = "",
        use_multitarget: bool = False,
        use_probabilities: bool = False,
    ):
        """
        Let's use calculate arbitrary classification
        metrics as part of the DataframeAnalyzer(ResultAnalyzer).

        Parameters
        ----------
        source_col: str
            name of the column with the class
            index or indexes (multitarget)
        target_cols_prefix: str
            starting name of the columns
            containing the output of the model
        function: str or dict, default "accuracy"
            function to calculate the metric.
            If str is given it must be a key of the `cl_metric_dict`.
            Otherwise the given dict is initialized with
            `init_object` and additional the key `name`
            must be available to define the
            output name in the result dict.
        name_suffix: str, default ""
            can be used to add a str to the dict
            output name (e.g. if the same metric should be applied
            to multiple columns)
        use_multitarget: bool, default false
            allows to be more than one class present per sample
        use_probabilities: bool, default false
            if this is set true then the values are
            not binarized before calculating the metric function
        """
        self.source_col = source_col
        self.target_cols_prefix = target_cols_prefix
        self.multi_target = use_multitarget
        self.name_suffix = name_suffix
        self.use_probabilities = use_probabilities
        if type(function) is str:
            self.func_name = function
            try:
                self.function = cl_metric_dict[function]
            except KeyError as e:
                raise Exception(
                    f"Function with name {function} not "
                    f"supported! Available: {list(cl_metric_dict.keys())}"
                ) from e
        else:
            self.func_name = function["name"]
            self.function = function["target"]

    def __call__(
        self, data: pd.DataFrame, exp_context: ExperimentContext, dataset_name: str
    ) -> dict:
        target_cols = [x for x in data.columns if x.startswith(self.target_cols_prefix)]
        array = data[target_cols].to_numpy()
        if self.multi_target:
            if not self.use_probabilities:
                binarized_array = np.round(array)
            else:
                binarized_array = array
            label_binarizer = MultiLabelBinarizer(classes=list(range(len(target_cols))))
            binarized_labels = label_binarizer.fit_transform(data[self.source_col])
            value = self.function(binarized_labels, binarized_array)
        else:
            if array.shape[1] == 1:
                if not self.use_probabilities:
                    pred_classes = np.round(array)
                else:
                    pred_classes = array
            else:
                pred_classes = np.argmax(array, axis=1)
            value = self.function(data[self.source_col], pred_classes)
        if isinstance(value, np.ndarray):
            value = value.tolist()
        else:
            value = float(value)
        return {f"{self.func_name}{self.name_suffix}": value}
