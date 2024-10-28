import numpy as np
import matplotlib.pyplot as plt
from typing import List, Literal
import matplotlib.ticker as mtick

# SUBGROUP = Literal["gender", "year_group", "fsm", "sen"]


def make_all_pupils_responses_graph(
    *,
    category_label: List[str],
    percentages: List[float],
    counts_list: List[int],
    topic: str,
    measure_label: str,
    legend_title: str = "Pupils",  # Default legend title
    legend_label: str = "All Pupils",  # Default legend label
) -> plt.Figure:
    """
    Generates a single bar chart for all pupils' responses.

    Args:
        category_label (List[str]): Labels for each category.
        percentages (List[float]): Percentage values for each category.
        counts_list (List[int]): Count values for each category.
        topic (str): The topic name.
        measure_label (str): The measure label.
        legend_title (str): The title for the legend. Defaults to "Pupils".
        legend_label (str): The label for the legend entry. Defaults to "All Pupils".

    Returns:
        plt.Figure: The generated matplotlib figure.
    """
    BAR_COLOUR = "#ea7555"
    BACKGROUND_COLOR = "#ffffff"

    fig, ax = plt.subplots(figsize=(10, 6))

    n_categories = len(category_label)
    index = np.arange(n_categories)
    bar_width = 0.7  # Same as in double bar chart

    # Plot the bars centered at index + bar_width / 2 to align with double bar chart
    bars = ax.bar(
        index + bar_width / 2,  # Shift to center
        percentages,
        bar_width,
        color=BAR_COLOUR,
        label=legend_label,  # Dynamic legend label
    )

    # Add labels, title, and legend
    ax.set_xlabel("Response")
    ax.set_ylabel("Percentage of pupils")
    ax.set_title(f"{measure_label}\n({topic})")
    ax.set_xticks(index + bar_width / 2)  # Align with double bar chart
    ax.set_xticklabels(
        category_label, rotation=-45, ha="left"
    )  # Consistent rotation and alignment

    # Add legend with title and without border
    ax.legend(
        loc="upper left",
        bbox_to_anchor=(1, 1),
        frameon=False,
        title=legend_title,
    )

    # Remove the frame (spines)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add faint horizontal gridlines only on y-axis
    ax.yaxis.grid(True, color="#EEEEEE")
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)

    # Format y-axis to show percentages without decimals
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    # Adjust y-axis limit to accommodate annotations
    max_percent = max(percentages, default=0)
    ax.set_ylim(0, max_percent + 10)  # Increase upper limit by 10% for annotations

    # Function to handle bar visibility and annotations
    def handle_bars(bars, counts, percentages):
        for bar, count, percent in zip(bars, counts, percentages):
            height = bar.get_height()
            if height == 0:
                bar.set_visible(False)
                continue  # Skip annotations for zero-height bars

            # Annotate count at the bottom inside the bar
            ax.annotate(
                f"n={count}",
                xy=(bar.get_x() + bar.get_width() / 2, 0),
                xytext=(0, 2),  # 2 points vertical offset
                textcoords="offset points",
                ha="center",
                va="bottom",
                color="black",
                fontsize=8,
            )
            # Annotate percentage above the bar
            ax.annotate(
                f"{percent:.1f}%",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                color="black",
            )

    # Handle annotations and visibility
    handle_bars(bars, counts=counts_list, percentages=percentages)

    # Set background color
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    fig.tight_layout()

    return fig


# Example usage
fig = make_all_pupils_responses_graph(
    category_label=["1", "2", "3", "4", "5"],
    percentages=[15.6, 21.1, 17.2, 16.4, 17.2],
    counts_list=[5, 7, 6, 4, 5],
    topic="Autonomy",
    measure_label="I feel pressured in my life",
    legend_title="Pupils",
    legend_label="All Pupils",
)

plt.show()
