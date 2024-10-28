import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Literal
import matplotlib.ticker as mtick

SUBGROUP = Literal["gender", "year_group", "fsm", "sen"]


def make_subgroup_comparison_graph(
    *,
    category_label: List[str],
    percentages: List[Tuple[float, float]],
    counts_list: List[Tuple[int, int]],
    topic: str,
    measure_label: str,
    comparison_groups: List[str],
    legend_title: str,  # Added legend_title parameter
) -> plt.Figure:
    LEFT_BAR_COLOUR = "#ea7555"
    RIGHT_BAR_COLOUR = "#f1b79f"
    BACKGROUND_COLOR = "#ffffff"

    fig, ax = plt.subplots(figsize=(10, 6))

    n_categories = len(category_label)
    index = np.arange(n_categories)
    bar_width = 0.35

    # Extract the left and right percentages
    left_percentages = [float(p[0]) for p in percentages]
    right_percentages = [float(p[1]) for p in percentages]

    print("Left percents:", left_percentages)
    print("Right percents:", right_percentages)
    print("Types in left_percentages:", [type(p) for p in left_percentages])
    print("Types in right_percentages:", [type(p) for p in right_percentages])

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
    ax.set_xlabel("Response")
    ax.set_ylabel("Percentage of pupils")
    ax.set_title(f"{measure_label}\n({topic})")
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(category_label, rotation=-45, ha="left")

    # Add legend with title and without border
    ax.legend(
        loc="upper left", bbox_to_anchor=(1, 1), frameon=False, title=legend_title
    )

    # Remove the frame (spines)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add faint horizontal gridlines
    ax.yaxis.grid(True, color="#EEEEEE")
    ax.set_axisbelow(True)

    # Format y-axis to show percentages and remove negative signs
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    # Ensure y-axis starts at 0
    ax.set_ylim(bottom=0)

    # Add percentages above the bars and counts at the bottom inside the bars
    left_counts = [c[0] for c in counts_list]
    right_counts = [c[1] for c in counts_list]

    # Adjust y-axis limit to accommodate annotations
    max_percent = max(max(left_percentages), max(right_percentages))
    ax.set_ylim(0, max_percent + 10)  # Increase upper limit by 10% for annotations

    for rect, count, percent in zip(bars1, left_counts, left_percentages):
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

    for rect, count, percent in zip(bars2, right_counts, right_percentages):
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


figure = make_subgroup_comparison_graph(
    category_label=[
        "1 - Completely not true",
        "2",
        "3",
        "4",
        "5 - Completely true",
        "No response",
    ],
    percentages=[
        (14.5, 17.3),
        (21.0, 17.3),
        (22.6, 15.4),
        (0.0, 21.2),
        (24.2, 11.5),
        (8.1, 0.0),
    ],
    counts_list=[(3, 4), (6, 4), (7, 5), (0, 11), (11, 6), (5, 0)],
    topic="Autonomy",
    measure_label="I feel pressured in my life",
    comparison_groups=["Year 8", "Year 10"],
    legend_title="Pupils",
)

# Display the figure
plt.show()
