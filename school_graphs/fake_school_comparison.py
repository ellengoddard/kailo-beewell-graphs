from school_gtaphs.comparison_graph import make_comparison_graph
from school_gtaphs.comparison_graph import School
import matplotlib.pyplot as plt

# Convert dictionaries to School objects
schools = [
    School(mean_topic_score=17.25),
    School(mean_topic_score=17.55),
    School(mean_topic_score=17.65),
    School(mean_topic_score=17.7),
    School(mean_topic_score=17.85),
    School(mean_topic_score=18.28),
    School(mean_topic_score=18.65),
]

range_low = 17
range_high = 19

y_label = "Mean Score"
x_label = "Northern Devon schools (ordered by mean score)"

below_avg_amount = 17.4
average_amount = 18.5
above_avg_amount = 18.2

current_school = School(mean_topic_score=17.25)

figure = make_comparison_graph(
    schools=schools,
    range_low=range_low,
    range_high=range_high,
    y_label=y_label,
    x_label=x_label,
    below_avg_amount=below_avg_amount,
    average_amount=average_amount,
    current_school=current_school, # School(mean_topic_score=17.25)
)

# Display the figure
plt.show()
