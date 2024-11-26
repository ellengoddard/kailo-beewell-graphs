"""Module to contain the responses double comparison graphs."""

from typing import Literal

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

SUBGROUP = Literal["gender", "year_group", "fsm", "sen"]


def make_subgroup_comparison_graph(  # noqa: PLR0913
    *,
    category_label: list[str],
    percentages: list[tuple[float, float]],
    counts_list: list[tuple[int, int]],
    topic: str,
    measure_label: str,
    comparison_groups: list[str],
    legend_title: str,  # Added legend_title parameter
) -> plt.Figure:
    """Make the dual-barred charts."""
    LEFT_BAR_COLOUR = "#ea7555"  # noqa: N806
    RIGHT_BAR_COLOUR = "#f1b79f"  # noqa: N806
    BACKGROUND_COLOR = "#ffffff"  # noqa: N806

    fig, ax = plt.subplots(figsize=(10, 6))

    n_categories = len(category_label)
    index = np.arange(n_categories)
    bar_width = 0.45

    # Extract the left and right percentages
    left_percentages = [float(p[0]) for p in percentages]
    right_percentages = [float(p[1]) for p in percentages]

    # Plot the bars with updated legend labels
    bars1 = ax.bar(
        index,
        left_percentages,
        bar_width,
        label=comparison_groups[0],
        color=LEFT_BAR_COLOUR,
    )
    bars2 = ax.bar(
        index + bar_width,
        right_percentages,
        bar_width,
        label=comparison_groups[1],
        color=RIGHT_BAR_COLOUR,
    )

    # Add labels, title, and legend
    ax.set_xlabel("Responses")
    ax.set_ylabel("Percentage of pupils")
    ax.set_title(f"{measure_label}\n({topic})", wrap=True)
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(category_label, rotation=-45, ha="left")

    # Add legend with title and without border
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1), frameon=False, title=legend_title)

    # Remove the frame (spines)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Don't show vertical gridlines, only horizontal ones
    ax.yaxis.grid(visible=True, color="#EEEEEE")  # Horizontal gridlines only
    ax.xaxis.grid(visible=False)  # No vertical gridlines
    ax.set_axisbelow(True)

    # Format y-axis to show percentages and remove negative signs
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    # Ensure y-axis starts at 0
    ax.set_ylim(bottom=0)

    # Add percentages above the bars and counts at the bottom inside the bars
    left_counts = [c[0] for c in counts_list]
    right_counts = [c[1] for c in counts_list]

    # Adjust y-axis limit to accommodate annotations
    max_percent = max(*left_percentages, *right_percentages)
    ax.set_ylim(0, max_percent + 10)  # Increase upper limit by 10% for annotations

    for rect, count, percent in zip(bars1, left_counts, left_percentages, strict=False):
        height = rect.get_height()
        # Annotate count at the bottom inside the bar
        ax.annotate(
            f"n={int(count)}" if count else "",
            xy=(rect.get_x() + rect.get_width() / 2, 0),
            xytext=(0, 2),  # 2 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
            color="black",
            fontsize=8,
        )
        # Annotate percentage above the bar, always show %, even if it's 0
        ax.annotate(
            f"{percent:.1f}%",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
            color="black",
        )

    for rect, count, percent in zip(bars2, right_counts, right_percentages, strict=False):
        height = rect.get_height()
        # Annotate count at the bottom inside the bar
        ax.annotate(
            # If count exists, show count otherwise show empty string (nothing)
            f"n={int(count)}" if count else "",
            xy=(rect.get_x() + rect.get_width() / 2, 0),
            xytext=(0, 2),
            textcoords="offset points",
            ha="center",
            va="bottom",
            color="black",
            fontsize=8,
        )
        # Annotate percentage above the bar, always show %, even if it's 0
        ax.annotate(
            f"{percent:.1f}%",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
            color="black",
        )

    # Set background color
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    fig.tight_layout()

    return fig
