"""Module containing classes which describe the sample experiments"""
import pandera as pa

from niceml.experiments.schemas.defaultexpschema import DefaultExperimentSchema
from niceml.experiments.schemas.parquetframeexpmember import ParquetMember


num_reg_df_schema = pa.DataFrameSchema(
    {
        "dataid": pa.Column(pa.Object),
        "px_0_0": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_0_1": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_0_2": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_0_3": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_0_4": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_0_5": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_0_6": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_0_7": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_0_8": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_0_9": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_1_0": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_1_1": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_1_2": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_1_3": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_1_4": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_1_5": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_1_6": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_1_7": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_1_8": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_1_9": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_2_0": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_2_1": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_2_2": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_2_3": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_2_4": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_2_5": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_2_6": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_2_7": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_2_8": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_2_9": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_3_0": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_3_1": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_3_2": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_3_3": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_3_4": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_3_5": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_3_6": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_3_7": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_3_8": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_3_9": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_4_0": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_4_1": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_4_2": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_4_3": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_4_4": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_4_5": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_4_6": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_4_7": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_4_8": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_4_9": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_5_0": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_5_1": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_5_2": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_5_3": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_5_4": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_5_5": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_5_6": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_5_7": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_5_8": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_5_9": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_6_0": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_6_1": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_6_2": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_6_3": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_6_4": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_6_5": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_6_6": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_6_7": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_6_8": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_6_9": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_7_0": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_7_1": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_7_2": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_7_3": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_7_4": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_7_5": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_7_6": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_7_7": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_7_8": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_7_9": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_8_0": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_8_1": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_8_2": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_8_3": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_8_4": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_8_5": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_8_6": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_8_7": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_8_8": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_8_9": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_9_0": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_9_1": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_9_2": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_9_3": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_9_4": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_9_5": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_9_6": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_9_7": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_9_8": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "px_9_9": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "label": pa.Column(pa.Float64, checks=pa.Check.in_range(0.0, 1.0)),
        "pred_0000": pa.Column(pa.Float32, checks=pa.Check.in_range(-1.0, 1.0)),
    }
)


class NumRegExpSchema(
    DefaultExperimentSchema
):  # pylint: disable=too-few-public-methods
    """This is the experiment for regression"""

    test_parq = ParquetMember(
        path="predictions/test.parq",
        description="Here the predictions of the numbers testset are stored.",
        required=True,
        df_schema=num_reg_df_schema,
    )

    valid_parq = ParquetMember(
        path="predictions/validation.parq",
        description="Here the predictions of the numbers validationset are stored.",
        required=True,
        df_schema=num_reg_df_schema,
    )

    train_parq = ParquetMember(
        path="predictions/train_eval.parq",
        description="Here the predictions of the numbers train eval set are stored.",
        required=True,
        df_schema=num_reg_df_schema,
    )


if __name__ == "__main__":
    print(NumRegExpSchema.__doc__, end="\n")
