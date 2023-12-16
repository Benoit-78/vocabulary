"""
    Creation date:
        16th December 2023
    Main purpose:

"""

import plotly.express as px
import plotly.io as pio


x_values = [1, 2, 3, 4]
y_values = [10, 11, 12, 13]

# Create a sample graph
fig = px.scatter(
    x=x_values,
    y=y_values,
    labels={
        'x':'X-axis',
        'y':'Y-axis'
    },
    title='Sample Scatter Plot'
)

# Convert the graph to HTML
graph_html = pio.to_html(fig, full_html=False)
