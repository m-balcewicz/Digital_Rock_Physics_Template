import numpy as np
from matplotlib import pyplot as plt
import barbara.default_parameters as params


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
    ax = fig.add_axes(params.x_axes_right)
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
    ax = fig.add_axes(params.x_axes_right)  # left, bottom, width, height

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


def shift_histogram(data_list, data_vars, data_ref, dtype='uint16', cmap_set=None, xlim=None, ylim=None, mask=None):
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
    ax = fig.add_axes(params.x_axes_right)  # left, bottom, width, height

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

    if xlim is None and ylim is None:
        plt.xlim([40000, 60000])
        plt.ylim([10e3, 10e4])
    elif isinstance(xlim, list) and len(xlim) == 2 and isinstance(xlim[0], (int, float)) and isinstance(xlim[1], (int, float)) and \
            isinstance(ylim, list) and len(ylim) == 2 and isinstance(ylim[0], (int, float)) and isinstance(ylim[1], (int, float)):
        plt.xlim(xlim)
        plt.ylim(ylim)
    else:
        raise ValueError("xlim and ylim must be lists of two integers.")

    if mask is None:
        raise ValueError("Please provide a mask value")
    elif isinstance(mask, list) and len(mask) == 2 and isinstance(mask[0], int) and isinstance(mask[1], int) and mask[0] < mask[1]:
        # Find the minimum and maximum values within the specified mask
        data_masked = np.ma.masked_where((data_ref < mask[0]) | (data_ref > mask[1]), data_list[0])
        data_min = np.min(data_masked)
        data_max = np.max(data_masked)

        # Find the most common value within the masked data
        data_flat = data_masked.flatten()
        bincount = np.bincount(data_flat)
        data_mode = np.argmax(bincount)

        max = data_min + data_mode

        print(f'data min in masked array: {data_min}')
        print(f'data max in masked array: {data_max}')
        print(f'data mode in masked array: {data_mode}')
        print(f'max in masked array: {max}')

        # Add vertical lines for the minimum and maximum values
        plt.axvline(x=max, color='g')

    else:
        raise ValueError("Mask must be a list of two integers with the first value smaller than the second value.")

    return fig
