"""Module containing classes which describe the sample experiments"""
import pandera as pa

from niceml.experiments.schemas.defaultexpschema import DefaultExperimentSchema
from niceml.experiments.schemas.parquetframeexpmember import ParquetMember

sin_reg_df_schema = pa.DataFrameSchema(
    {
        "dataid": pa.Column(pa.Float, checks=pa.Check.in_range(0.0, 20.0)),
        "xs": pa.Column(pa.Float, checks=pa.Check.in_range(0.0, 20.0)),
        "ys": pa.Column(pa.Float, checks=pa.Check.in_range(-1.0, 1.0)),
        "pred_0000": pa.Column(pa.Float32, checks=pa.Check.in_range(-1.0, 1.0)),
    }
)


class SinRegExpSchema(
    DefaultExperimentSchema
):  # pylint: disable=too-few-public-methods
    """This is the experiment for regression"""

    test_parq = ParquetMember(
        path="predictions/test.parq",
        description="Here the predictions of the sinus testset are stored.",
        required=True,
        df_schema=sin_reg_df_schema,
    )

    valid_parq = ParquetMember(
        path="predictions/validation.parq",
        description="Here the predictions of the sinus validationset are stored.",
        required=True,
        df_schema=sin_reg_df_schema,
    )

    train_parq = ParquetMember(
        path="predictions/train_eval.parq",
        description="Here the predictions of the sinus train eval set are stored.",
        required=True,
        df_schema=sin_reg_df_schema,
    )


if __name__ == "__main__":
    print(SinRegExpSchema.__doc__, end="\n")
