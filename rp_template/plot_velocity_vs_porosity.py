import matplotlib.pyplot as plt
import numpy as np

import drp_template.default_parameters as params
from cmcrameri import cm

def velocity_vs_porosity(porosity, VP, VS, samples, legend_location='best', legend_bbox_to_anchor=(1, 1)):
    """
    porosity = [...]  # list or array of porosity values
    VP = [...]  # list or array of VP values
    VS = [...]  # list or array of VS values

    """
    params.default_data_figure()
    fig = plt.figure()
    plt.xlabel('Porosity (%)')
    plt.ylabel('Effective velocity (m/s)')

    cmap = cm.batlow
    markers = ['o', 's', '^', 'v', 'D', 'p', '*', 'h', 'x', '+', '1', '2', '3', '4', '8', 's', 'd', 'h', 'H', 'P']


    scatter_plots = []  # List to store scatter plots for the legend

    for i in range(len(porosity)):
        color = cmap(i / len(porosity))  # Get color from the colormap
        marker = markers[i % len(markers)]  # Get marker for scatter plot

        vp_plot = plt.scatter(porosity[i], VP[i], c=[color], marker=marker, s=100)
        vs_plot = plt.scatter(porosity[i], VS[i], c='none', marker=marker, s=100, edgecolors=np.array([color]), linewidths=2)

        scatter_plots.append(vp_plot)  # Add scatter plot to the list for the legend

    # Create a legend using the scatter plots and the corresponding labels from 'samples'
    plt.legend(scatter_plots, samples, loc=legend_location, bbox_to_anchor=legend_bbox_to_anchor)

    # Set x-axis limits to 10% above and below the highest and lowest values
    min_value_x = min(np.min(porosity), np.min(porosity))
    max_value_x = max(np.max(porosity), np.max(porosity))
    x_range = max_value_x - min_value_x
    x_margin = 0.1 * x_range
    plt.xlim(min_value_x - x_margin, max_value_x + x_margin)

    # Set y-axis limits to 10% above and below the highest and lowest values
    min_value_y = min(np.min(VP), np.min(VS))
    max_value_y = max(np.max(VP), np.max(VS))
    y_range = max_value_y - min_value_y
    y_margin = 0.1 * y_range
    plt.ylim(min_value_y - y_margin, max_value_y + y_margin)

    # # Set y-axis tick positions at 500 steps
    # y_ticks = np.arange(np.floor(min_value_y / 500) * 500, np.ceil(max_value_y / 500) * 500 + 500, 500)
    # plt.yticks(y_ticks)

    # Add minor grid lines
    plt.grid(True, which='both', linestyle='dotted', linewidth=0.5)

    return fig
