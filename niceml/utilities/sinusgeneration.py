"""Module for Sinus generation for example data"""
import numpy as np
import pandas as pd

from niceml.data.dataloaders.interfaces.dfloader import DfLoader


def generate_sinus_df(
    sample_count: int, seed: int = 1234, min_x: float = 0, max_x: float = 1
) -> pd.DataFrame:
    """
    Generates a dataframe with two columns:
        - xs: random floats between min_x and max_x
        - ys: sinus of the x values

    Args:
        sample_count: Number of samples to be generated
        seed: Seed for the random number generator
        min_x: Set the minimum value of x
        max_x: Set the maximum value of x
    Returns:
         Dataframe with the two generated columns
    """
    rng = np.random.default_rng(seed=seed)
    x_values = rng.uniform(min_x, max_x, sample_count)
    y_values = np.sin(x_values)
    return pd.DataFrame(dict(xs=x_values, ys=y_values))


class SinusDfLoader(DfLoader):  # pylint: disable=too-few-public-methods
    """DfLoader which returns a generated sinus dataframe"""

    def __init__(self, sample_count, seed: int, min_x: float, max_x: float):
        self.sample_count = sample_count
        self.seed = seed
        self.min_x = min_x
        self.max_x = max_x

    # pylint: disable=unused-argument
    def load_df(self, *args, **kwargs) -> pd.DataFrame:
        """Generates and returns a dataframe with sinus values"""
        return generate_sinus_df(self.sample_count, self.seed, self.min_x, self.max_x)
