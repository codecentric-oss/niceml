from typing import List

from pydantic import Field

from niceml.dagster.ops.analysis import AnalysisConfig
from niceml.config.hydra import InitConfig
from niceml.mlcomponents.resultanalyzers.dataframes.clsmetric import ClsMetric
from niceml.mlcomponents.resultanalyzers.dataframes.dfanalyzer import DataframeAnalyzer


class ConfResultAnalyzer(InitConfig):
    """This class configures the result analyzer"""

    target: str = InitConfig.create_target_field(DataframeAnalyzer)


class ConfClsMetricAccuracy(InitConfig):
    """This class configures the accuracy metric"""

    target: str = InitConfig.create_target_field(ClsMetric)
    function: str = "accuracy"
    source_col: str = "class_idx"
    target_cols_prefix: str = "pred_"


class ConfClsMetricConfusionMatrix(ConfClsMetricAccuracy):
    """This class configures the confusion matrix metric"""

    function: str = "confusion_matrix"


class ConfOpAnalysisClsSoftmax(AnalysisConfig):
    """This class configures the analysis op for classification with softmax"""

    result_analyzer: ConfResultAnalyzer = Field(
        default_factory=ConfResultAnalyzer,
        description="Result analyzer",
        alias="result_analyzer",
    )
    metrics: List[InitConfig] = [
        ConfClsMetricAccuracy(),
        ConfClsMetricConfusionMatrix(),
    ]
