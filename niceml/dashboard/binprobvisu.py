"""Module for the ProbDistributionChartGenerator"""

from dataclasses import dataclass
from typing import Any, Optional, Tuple

import altair
import numpy as np
import pandas as pd

from niceml.utilities.chartutils import generate_hover_charts


# Quest: Still useful?
# pylint:disable = too-many-instance-attributes
@dataclass
class ProbDistributionChartGenerator:
    """Generates a chart for a probability distribution."""

    prob_col: str
    gt_col: str
    pos_gt_val: Any
    neg_gt_val: Any
    range_min: float = 0.0
    range_max: float = 1.0
    bin_count: int = 20
    pos_gt_name: Optional[str] = None
    neg_gt_name: Optional[str] = None
    x_name: str = "probability"
    y_name: str = "count"
    chart_width: int = 800
    chart_height: int = 500
    pos_color: str = "#41b545"
    neg_color: str = "#ff450d"

    # pylint:disable = too-many-locals, too-many-statements
    def __call__(
        self, prob_df: pd.DataFrame, thres_min: float, thres_max: float
    ) -> Tuple[altair.Chart, pd.DataFrame]:
        """
        Takes in a dataframe with probabilities and ground truth values, as well as two thresholds
        (thres_min and thres_max). It returns an altair histogram chart that visualize
        the prediction probability. The second return value is a dataframe containing
        metrics for the given thresholds.

        Args:
            prob_df: pd.DataFrame: Pass in the dataframe that contains the probabilities
                        and ground truth values
            thres_min: float: Set the minimum threshold for the histogram
            thres_max: float: Set the upper bound of the threshold

        Returns:
            A tuple of two elements, the first being a chart and the second being a dataframe
        """
        pos_gt_name = self.pos_gt_val if self.pos_gt_name is None else self.pos_gt_name
        neg_gt_name = self.neg_gt_val if self.neg_gt_name is None else self.neg_gt_name
        pos_probs = prob_df[self.prob_col][prob_df[self.gt_col] == self.pos_gt_val]
        pos_count = len(pos_probs)
        neg_probs = prob_df[self.prob_col][prob_df[self.gt_col] == self.neg_gt_val]
        neg_count = len(neg_probs)

        pos_prob_hist = np.histogram(
            pos_probs, self.bin_count, range=(self.range_min, self.range_max)
        )
        neg_prob_hist = np.histogram(
            neg_probs, self.bin_count, range=(self.range_min, self.range_max)
        )
        # same for both
        hist_x_vals = neg_prob_hist[1]
        # mean of both borders
        prob_x_values = [
            (hist_x_vals[x] + hist_x_vals[x + 1]) / 2 for x in range(self.bin_count)
        ]

        df_pos_plot = pd.DataFrame(
            {
                self.y_name: pos_prob_hist[0],
                self.x_name: prob_x_values,
                "name": [pos_gt_name] * len(prob_x_values),
            }
        )

        df_neg_plot = pd.DataFrame(
            {
                self.y_name: neg_prob_hist[0],
                self.x_name: prob_x_values,
                "name": [neg_gt_name] * len(prob_x_values),
            }
        )
        concat_df_plot = pd.concat([df_pos_plot, df_neg_plot], ignore_index=True)
        domain = [pos_gt_name, neg_gt_name]
        color_range = [self.pos_color, self.neg_color]
        line_chart = (
            altair.Chart(concat_df_plot)
            .mark_line()
            .encode(
                x=self.x_name,
                y=self.y_name,
                color=altair.Color(
                    "name", scale=altair.Scale(domain=domain, range=color_range)
                ),
            )
        )

        thres_min_df = pd.DataFrame([{"thres_min": thres_min}])
        thres_max_df = pd.DataFrame([{"thres_max": thres_max}])

        thres_min_chart = (
            altair.Chart(thres_min_df).mark_rule(color="gray").encode(x="thres_min")
        )
        thres_max_chart = (
            altair.Chart(thres_max_df).mark_rule(color="gray").encode(x="thres_max")
        )

        hover_chart = generate_hover_charts(
            concat_df_plot,
            self.x_name,
            self.y_name,
            line_chart,
            self.chart_width,
            self.chart_height,
            [thres_min_chart, thres_max_chart],
        )

        true_neg_count = 0
        false_pos_count = 0
        false_check_count = 0
        true_pos_count = 0
        false_neg_count = 0
        true_check_count = 0
        for idx, x_val in enumerate(prob_x_values):
            if x_val <= thres_min:
                true_neg_count += neg_prob_hist[0][idx]
                false_neg_count += pos_prob_hist[0][idx]
            elif thres_min < x_val < thres_max:
                false_check_count += neg_prob_hist[0][idx]
                true_check_count += pos_prob_hist[0][idx]
            elif x_val >= thres_max:
                false_pos_count += neg_prob_hist[0][idx]
                true_pos_count += pos_prob_hist[0][idx]

        true_pos_perc = float(true_pos_count / pos_count)
        true_neg_perc = float(true_neg_count / neg_count)
        false_neg_perc = float(false_neg_count / pos_count)
        false_pos_perc = float(false_pos_count / neg_count)
        true_check_perc = float(true_check_count / pos_count)
        false_check_perc = float(false_check_count / neg_count)

        true_dict = {
            "class": pos_gt_name,
            pos_gt_name: true_pos_count,
            neg_gt_name: false_neg_count,
            "check": true_check_count,
            f"{pos_gt_name}_perc": true_pos_perc,
            f"{neg_gt_name}_perc": false_neg_perc,
            "check_perc": true_check_perc,
            "count": pos_count,
        }

        false_dict = {
            "class": neg_gt_name,
            pos_gt_name: false_pos_count,
            neg_gt_name: true_neg_count,
            "check": false_check_count,
            f"{pos_gt_name}_perc": false_pos_perc,
            f"{neg_gt_name}_perc": true_neg_perc,
            "check_perc": false_check_perc,
            "count": neg_count,
        }

        total_pos = false_pos_count + true_pos_count
        total_neg = true_neg_count + false_neg_count
        total_check = false_check_count + true_check_count
        total_count = pos_count + neg_count

        total_dict = {
            "class": "total",
            pos_gt_name: total_pos,
            neg_gt_name: total_neg,
            "check": total_check,
            f"{pos_gt_name}_perc": total_pos / total_count,
            f"{neg_gt_name}_perc": total_neg / total_count,
            "check_perc": total_check / total_count,
            "count": total_count,
        }

        metric_df = pd.DataFrame([true_dict, false_dict, total_dict])

        return hover_chart, metric_df
