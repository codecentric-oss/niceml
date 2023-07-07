"""Module for object detection experiment schema"""
import pandera as pa

from niceml.experiments.schemas.defaultexpschema import DefaultExperimentSchema
from niceml.experiments.schemas.parquetframeexpmember import ParquetMember

obj_det_df_schema = pa.DataFrameSchema(
    {
        "image_location": pa.Column(pa.String),
        "detection_index": pa.Column(pa.Int),
        "x_pos": pa.Column(pa.Float),
        "y_pos": pa.Column(pa.Float),
        "width": pa.Column(pa.Float),
        "height": pa.Column(pa.Float),
        "pred_0000": pa.Column(pa.Float, checks=pa.Check.in_range(-1.0, 1.0)),
    }
)


class ObjDetExpSchema(
    DefaultExperimentSchema
):  # pylint: disable=too-few-public-methods
    """This is the experiment for object detection"""

    test_parq = ParquetMember(
        path="predictions/test.parq",
        description="Here the predictions of the objdet testset are stored.",
        required=True,
        df_schema=obj_det_df_schema,
    )

    valid_parq = ParquetMember(
        path="predictions/validation.parq",
        description="Here the predictions of the objdet validationset are stored.",
        required=True,
        df_schema=obj_det_df_schema,
    )

    train_parq = ParquetMember(
        path="predictions/train_eval.parq",
        description="Here the predictions of the objdet train eval set are stored.",
        required=True,
        df_schema=obj_det_df_schema,
    )
