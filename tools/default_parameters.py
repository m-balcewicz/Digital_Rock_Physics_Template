import matplotlib.pyplot as plt
from cmcrameri import cm

# specific parameters for figures
figsize = (10, 6)
x_axes_right = [0.15, 0.11, 0.75, 0.8]         # left, bottom, width, height
x_axes_left = [0.085, 0.11, 0.75, 0.8]         # left, bottom, width, height
l_axes = [0.22, 0.11, 0.03, 0.8]         # preliminary for the colorbar: on the left side
r_axes = [0.735, 0.11, 0.03, 0.8]         # preliminary for the colorbar: on the right side
# colormap after:  Crameri, Fabio: Scientific colour maps, https://zenodo.org/record/1243862, (2021)
cmap = cm.batlow                         # default colormap
linewidth = 2
linecolor = 'white'


def default_figure():
    # set the default figure size
    plt.rcParams['figure.figsize'] = (10, 6)

    # set the background color of the figure
    plt.rcParams['figure.facecolor'] = 'white'

    # set the default x-axes position
    plt.rcParams['figure.subplot.left'] = 0.15          # left
    plt.rcParams['figure.subplot.bottom'] = 0.11        # bottom
    plt.rcParams['figure.subplot.right'] = 0.75         # width
    plt.rcParams['figure.subplot.top'] = 0.8            # height

    # set the font family and size
    # plt.rcParams['font.family'] = 'Courier New'
    # plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 20

def default_data_figure():
    # set the default figure size
    plt.rcParams['figure.figsize'] = (12, 7)

    # set the background color of the figure
    plt.rcParams['figure.facecolor'] = 'white'

    # set the default x-axes position
    plt.rcParams['figure.subplot.left'] = 0.15          # left
    plt.rcParams['figure.subplot.bottom'] = 0.11        # bottom
    plt.rcParams['figure.subplot.right'] = 0.75         # width
    # plt.rcParams['figure.subplot.top'] = 0.8            # height

    # set the font family and size
    # plt.rcParams['font.family'] = 'Courier New'
    # plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 20
