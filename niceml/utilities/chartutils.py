from typing import List, Optional

import altair


def generate_hover_charts(  # QUEST: still in use?
    source,
    x_name: str,
    text_name: str,
    base_chart,
    width: int,
    height: int,
    additional_layers: Optional[List[altair.Chart]] = None,
    text_type: str = "Q",
):
    """Generates Altair Charts, with hover functionality"""
    if additional_layers is None:
        additional_layers = []
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = altair.selection(
        type="single", nearest=True, on="mouseover", fields=[x_name], empty="none"
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = (
        altair.Chart(source)
        .mark_point()
        .encode(
            x=x_name,
            opacity=altair.value(0),
        )
        .add_selection(nearest)
    )

    # Draw points on the line, and highlight based on selection
    points = base_chart.mark_point().encode(
        opacity=altair.condition(nearest, altair.value(1), altair.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = base_chart.mark_text(align="left", dx=5, dy=-5).encode(
        text=altair.condition(nearest, f"{text_name}:{text_type}", altair.value(" "))
    )

    # Draw a rule at the location of the selection
    rules = (
        altair.Chart(source)
        .mark_rule(color="gray")
        .encode(x=f"{x_name}:Q")
        .transform_filter(nearest)
    )

    return altair.layer(
        base_chart, selectors, points, rules, text, *additional_layers
    ).properties(width=width, height=height)


def generate_chart(source, metric):  # TODO: rename function and add docstrings
    line = (
        altair.Chart(source)
        .mark_line()
        .encode(
            x="epoch",
            y=metric,
            color="name",
        )
    )

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = altair.selection(
        type="single", nearest=True, on="mouseover", fields=["epoch"], empty="none"
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = (
        altair.Chart(source)
        .mark_point()
        .encode(
            x="epoch",
            opacity=altair.value(0),
        )
        .add_selection(nearest)
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=altair.condition(nearest, altair.value(1), altair.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align="left", dx=5, dy=-5).encode(
        text=altair.condition(nearest, f"{metric}:Q", altair.value(" "))
    )

    # Draw a rule at the location of the selection
    rules = (
        altair.Chart(source)
        .mark_rule(color="gray")
        .encode(
            x="epoch:Q",
        )
        .transform_filter(nearest)
    )

    return altair.layer(line, selectors, points, rules, text).properties(
        width=600, height=400
    )
