import numpy as np
from matplotlib import pyplot as plt
import drp_template.default_parameters as params


def plot_histogram(data, dtype='uint16'):
    if dtype == 'uint8':
        gray_max = 255
    elif dtype == 'uint16':
        gray_max = 65535

    params.default_figure()

    # Calculate maximum number of data points for histogram
    # max_data_points = len(np.unique(data))
    # bins_guess = int(np.sqrt(max_data_points))
    bins_guess = 255

    # Compute histogram of gray-scale intensities
    print(f'calculating bins . . .')
    hist, bins = np.histogram(data, bins=bins_guess, range=(0, gray_max))

    # Create a color map for the histogram bars
    cmap = params.cmap
    colors = cmap(np.linspace(0, 1, len(bins)))

    # Plot histogram as a line plot
    fig = plt.figure(figsize=params.figsize)
    ax = fig.add_axes(params.x_axes)
    ax.plot(bins[:-1], hist, color=params.linecolor, linewidth=params.linewidth)

    # Plot histogram using colored bars
    ax.bar(bins[:-1], hist, width=bins[1] - bins[0], color=colors[:-1], linewidth=0.5)

    ax.set_yscale('log')  # Set y-axis to logarithmic scale
    ax.set_xlabel('Gray-scale intensity')
    ax.set_ylabel('Frequency')

    return fig


def compare_histograms(data_list, data_vars, dtype='uint16', cmap_set=None):
    if dtype == 'uint8':
        gray_max = 255
    elif dtype == 'uint16':
        gray_max = 65535

    if cmap_set is None:
        cmap_set = params.cmap
    else:
        cmap_set = cmap_set

    params.default_figure()

    # Calculate maximum number of data points for histogram
    # max_data_points = max(len(np.unique(data)) for data in data_list)
    # bins_guess = int(np.sqrt(max_data_points))
    bins_guess = 255

    # Create a color map for the line plot
    colors = cmap_set(np.linspace(0, 1, len(data_list)))

    fig = plt.figure(figsize=params.figsize)
    ax = fig.add_axes(params.x_axes)  # left, bottom, width, height

    for i, data in enumerate(data_list):
        print(f'calculating bins . . . for {data_vars[i]}')
        # Compute histogram of gray-scale intensities
        hist, bins = np.histogram(data, bins=bins_guess, range=(0, gray_max))

        # Plot histogram as a line plot
        # color = plt.cm.get_cmap('hsv')(i / len(data_list))
        ax.plot(bins[:-1], hist, color=colors[i], linewidth=params.linewidth, label=f'{data_vars[i]}')

    ax.set_yscale('log')  # Set y-axis to logarithmic scale
    ax.set_xlabel('Gray-scale intensity')
    ax.set_ylabel('Frequency')

    # create the legend and set its appearance
    leg = plt.legend(loc='upper right', frameon=True)
    for line in leg.get_lines():
        line.set_linewidth(5.0)  # set the width of each legend line

    return fig
