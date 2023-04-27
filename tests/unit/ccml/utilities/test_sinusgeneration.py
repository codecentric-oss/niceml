import numpy as np
import pandas as pd

from niceml.utilities.sinusgeneration import generate_sinus_df


def test_generate_sinus_df():
    values: pd.DataFrame = generate_sinus_df(1000, min_x=-10, max_x=10)
    assert min(values["xs"]) < -9.0
    assert max(values["xs"]) > 9.0
    assert min(values["ys"]) >= -1.0
    assert max(values["ys"]) <= 1.0
    assert len(values["xs"]) == 1000


def test_generate_sinus_df_twice():
    values1: pd.DataFrame = generate_sinus_df(1000)
    values2: pd.DataFrame = generate_sinus_df(1000)
    arr1 = values1.to_numpy()
    arr2 = values2.to_numpy()

    assert np.array_equal(arr1, arr2)
