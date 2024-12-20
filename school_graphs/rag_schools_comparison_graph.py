"""Code to generate the graphs that compare RAG ratings between schools.

Not to be confused with the double comparison graphs showing school-level responses.
"""

from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoLocator, FuncFormatter


@dataclass
class School:
    """Used to compare objects in this module."""

    mean_topic_score: float
    school_name: str | None = None


def make_comparison_graph(  # noqa: PLR0913
    *,
    schools: list[School],  # ordered by mean score
    range_low: float,
    range_high: float,
    y_label: str,
    x_label: str,
    below_avg_amount: float,
    above_avg_amount: float,
    current_school: School,
) -> plt.Figure:
    """Make the main RAG graphs."""
    CURRENT_SCHOOL_COLOR = "#5D98AB"  # noqa: N806
    OTHER_SCHOOL_COLOR = "#BFD8E0"  # noqa: N806
    RECTANGLE_ALPHA = 0.20  # noqa: N806
    BACKGROUND_COLOR = "#f4eee8"  # noqa: N806
    fig, ax = plt.subplots()

    # Set the background color
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    # Add horizontal rectangles to show the average score ranges
    ax.fill_between(
        x=[-0.5, len(schools) - 0.5],
        y1=range_low,
        y2=below_avg_amount,
        color="red",
        alpha=RECTANGLE_ALPHA,
        label="Below average",
    )
    ax.fill_between(
        x=[-0.5, len(schools) - 0.5],
        y1=below_avg_amount,
        y2=above_avg_amount,
        color="yellow",
        alpha=RECTANGLE_ALPHA,
        label="Average",
    )
    ax.fill_between(
        x=[-0.5, len(schools) - 0.5],
        y1=above_avg_amount,
        y2=range_high,
        color="green",
        alpha=RECTANGLE_ALPHA,
        label="Above average",
    )

    # Create bar chart
    scores = [school.mean_topic_score for school in schools]
    colors = [
        OTHER_SCHOOL_COLOR if school.school_name != current_school.school_name else CURRENT_SCHOOL_COLOR
        for school in schools
    ]
    _bars = ax.bar(range(len(schools)), scores, color=colors, alpha=1)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_ylim(range_low, range_high)
    ax.set_xticks([])  # Remove x-axis labels for each school
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(AutoLocator())

    # Custom formatter for y-axis tick labels
    def custom_formatter(x: int | str, _a) -> str:  # noqa: ANN001
        if x.is_integer():
            return f"{int(x)}"
        return f"{x:.2f}"

    ax.yaxis.set_major_formatter(FuncFormatter(custom_formatter))

    # Remove chart borders
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    # Customize the legend
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor=CURRENT_SCHOOL_COLOR, edgecolor="none", label="Your school"),
        Patch(facecolor=OTHER_SCHOOL_COLOR, edgecolor="none", label="Other schools"),
    ]
    # Place the legend in the upper right corner, outside the plot area
    fig.legend(
        title="Schools",
        handles=legend_elements,
        loc="outside right upper",
        frameon=False,
    )

    return fig
