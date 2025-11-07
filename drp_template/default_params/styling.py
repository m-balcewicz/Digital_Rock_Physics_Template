"""
Styling utilities for console output and matplotlib figures.

This module provides functions for formatted console printing and setting
matplotlib figure defaults.
"""

import matplotlib.pyplot as plt


__all__ = [
    'print_style',
    'default_figure',
    'default_data_figure'
]


def print_style(message, style='indented_separator'):
    """Print the given message with a specified style."""
    if style == 'box':
        style_chars = '#'
    elif style == 'section':
        style_chars = '='
    elif style == 'decorative':
        style_chars = '*'
    elif style == 'indented_separator':
        style_chars = '-'
    else:
        # Default to a simple line separator
        style_chars = '-'

    lines = message.split('\n')  # Split the multiline message into lines

    max_line_length = max(len(line) for line in lines)

    print(f"{style_chars * max_line_length}")
    for line in lines:
        # Pad shorter lines with spaces to match the maximum length
        print(f"{line.ljust(max_line_length)}")
    print(f"{style_chars * max_line_length}")


# Matplotlib figure defaults
# Colormap after: Crameri, Fabio: Scientific colour maps, https://zenodo.org/record/1243862, (2021)

def default_figure():
    """
    Set default matplotlib figure parameters for standard plots.
    
    Sets figure size, background color, subplot positions, and font size.
    """
    # set the default figure size
    plt.rcParams['figure.figsize'] = (10, 6)

    # set the background color of the figure
    plt.rcParams['figure.facecolor'] = 'white'

    # set the default x-axes position
    plt.rcParams['figure.subplot.left'] = 0.15          # left
    plt.rcParams['figure.subplot.bottom'] = 0.11        # bottom
    plt.rcParams['figure.subplot.right'] = 0.75         # width
    plt.rcParams['figure.subplot.top'] = 0.8            # height

    # set the font size
    plt.rcParams['font.size'] = 20


def default_data_figure():
    """
    Set default matplotlib figure parameters for data visualization plots.
    
    Sets figure size, background color, subplot positions, and font size.
    Slightly larger than default_figure for data-heavy plots.
    """
    # set the default figure size
    plt.rcParams['figure.figsize'] = (12, 7)

    # set the background color of the figure
    plt.rcParams['figure.facecolor'] = 'white'

    # set the default x-axes position
    plt.rcParams['figure.subplot.left'] = 0.15          # left
    plt.rcParams['figure.subplot.bottom'] = 0.11        # bottom
    plt.rcParams['figure.subplot.right'] = 0.75         # width

    # set the font size
    plt.rcParams['font.size'] = 20
