import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.colors import ListedColormap
from cmcrameri import cm

from drp_template.default_params import read_parameters_file, check_output_folder
from drp_template.image._config import global_settings, fig_width, fig_height

__all__ = [
    'histogram',
    'plot_effective_modulus',
    'get_figure_colors',
    'save_figure',
]


def _resolve_colormap(cmap_input):
    """
    Resolve a colormap name or object to a matplotlib Colormap.
    """
    if cmap_input is None:
        return plt.colormaps['viridis']

    # Already a Colormap-like object
    if hasattr(cmap_input, 'N') or callable(cmap_input):
        return cmap_input

    if isinstance(cmap_input, str):
        # First try matplotlib colormaps
        try:
            return plt.colormaps.get_cmap(cmap_input)
        except Exception:
            # Then try cmcrameri
            try:
                return getattr(cm, cmap_input)
            except Exception:
                if cmap_input.startswith('cm.'):
                    name = cmap_input.split('.', 1)[1]
                    try:
                        return getattr(cm, name)
                    except Exception:
                        try:
                            return plt.colormaps.get_cmap(name)
                        except Exception:
                            return plt.colormaps['viridis']
                else:
                    return plt.colormaps['viridis']

    return plt.colormaps['viridis']


def histogram(
    data,
    thresholds=None,
    paramsfile='parameters.json',
    dtype=None,
    cmap_set=None,
    title=None,
    log_scale='both',
    dark_mode=True,
    num_bins=None
):
    """
    Plot a histogram with optional threshold-based coloring.
    """
    # Flatten data if it's multidimensional
    data = data.flatten()

    # Set dtype based on the parameters file if not provided
    if dtype is None:
        dtype = read_parameters_file(paramsfile=paramsfile, paramsvars='dtype')

    # Determine gray_max based on dtype
    gray_max = 255 if dtype == 'uint8' else 65535

    # Set default colormap if not specified
    if cmap_set is None:
        cmap_val = global_settings.get('colormap', 'cm.batlow')
        cmap_set = _resolve_colormap(cmap_val)
    else:
        if isinstance(cmap_set, str):
            cmap_set = _resolve_colormap(cmap_set)

    # Set color scheme based on dark_mode
    if dark_mode:
        text_color, face_color, edge_color = 'white', 'black', 'white'
    else:
        text_color, face_color, edge_color = 'black', 'white', 'black'

    # Calculate histogram bins
    if num_bins is not None:
        bins = np.linspace(0, gray_max, num_bins + 1)
    else:
        # Calculate histogram bins using Freedman-Diaconis rule with guards
        iqr = np.percentile(data, 75) - np.percentile(data, 25)
        if iqr <= 0 or np.isnan(iqr):
            bins = np.linspace(0, gray_max, 256 + 1)
        else:
            bins_width = 2 * iqr / (len(data) ** (1 / 3))
            if not np.isfinite(bins_width) or bins_width <= 0:
                bins = np.linspace(0, gray_max, 256 + 1)
            else:
                bins = np.arange(0, gray_max + bins_width, bins_width)

    # Compute histogram of gray-scale intensities
    hist, bins = np.histogram(data, bins=bins, range=(0, gray_max))
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_widths = bins[1:] - bins[:-1]

    # protect log-scale plotting from zero counts
    hist_plot = hist.copy()
    if log_scale in ('both', 'y'):
        eps = 1e-6
        hist_plot = np.where(hist_plot <= 0, eps, hist_plot)

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor=face_color, edgecolor=edge_color)

    # Normalize thresholds to canonical list-of-dicts format
    if isinstance(thresholds, dict):
        thresholds = [{'label': k, 'range': tuple(v)} for k, v in thresholds.items()]

    if thresholds is not None:
        if not isinstance(thresholds, list):
            raise TypeError("'thresholds' must be a list of dicts with keys 'label' and 'range' or None")
        for t in thresholds:
            if not isinstance(t, dict):
                raise TypeError("Each threshold must be a dict with keys 'label' and 'range'")
            if 'label' not in t or 'range' not in t:
                raise KeyError("Each threshold dict must contain 'label' and 'range'")
            if not isinstance(t['label'], str):
                raise TypeError("threshold 'label' must be a string")
            if not (isinstance(t['range'], (list, tuple)) and len(t['range']) == 2):
                raise ValueError("threshold 'range' must be a sequence of two values (min,max)")

    # Plot histogram
    if thresholds is None:
        cmap = cmap_set if hasattr(cmap_set, 'N') else plt.colormaps.get_cmap(cmap_set)
        colors = cmap(np.linspace(0, 1, len(bins) - 1))
        ax.bar(bins[:-1], hist_plot, width=bin_widths, color=colors, linewidth=0.5, edgecolor=None)
    else:
        cmap = cmap_set if hasattr(cmap_set, 'N') else plt.colormaps.get_cmap(cmap_set)
        n_thresholds = len(thresholds)
        threshold_colors = [cmap(i / (n_thresholds - 1)) if n_thresholds > 1 else cmap(0.5)
                           for i in range(n_thresholds)]

        default_color = 'gray' if dark_mode else 'lightgray'
        bar_colors = [default_color] * len(bin_centers)

        for i, t in enumerate(thresholds):
            min_val, max_val = t['range']
            in_range = (bin_centers >= min_val) & (bin_centers <= max_val)
            for idx, flag in enumerate(in_range):
                if flag:
                    bar_colors[idx] = threshold_colors[i]

        for center, height, width, color in zip(bin_centers, hist_plot, bin_widths, bar_colors):
            ax.bar(center, height, width=width, color=color, edgecolor=None)

        legend_elements = [plt.Rectangle((0, 0), 1, 1, color=threshold_colors[i], label=t['label'])
                          for i, t in enumerate(thresholds)]
        ax.legend(handles=legend_elements, loc='upper right', 
                 facecolor=face_color, edgecolor=edge_color, framealpha=0.7)

    if log_scale in ('both', 'y'):
        try:
            min_positive = np.min(hist[hist > 0])
            ax.set_ylim(bottom=max(1e-6, min_positive * 0.1))
        except Exception:
            ax.set_ylim(bottom=1e-6)

    if log_scale == 'both':
        ax.set_xscale('log')
        ax.set_yscale('log')
    elif log_scale == 'x':
        ax.set_xscale('log')
    elif log_scale == 'y':
        ax.set_yscale('log')
        ax.set_ylim(bottom=0.1)

    font_size = plt.rcParams['font.size']
    ax.set_xlabel('Gray-scale intensity', color=text_color, fontsize=font_size)
    ax.set_ylabel('Frequency', color=text_color, fontsize=font_size)

    title_text = 'Threshold Histogram' if title is None else title
    ax.set_title(title_text, color=text_color, fontsize=font_size)

    ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, colors=text_color)

    for spine in ax.spines.values():
        spine.set_edgecolor(edge_color)

    ax.set_facecolor(face_color)

    return fig, ax


def plot_effective_modulus(
    fraction, data, types='avg', marker='o', markersize=4, dark_mode=False, cmap_set=None, 
    xlabel_percent=False, grid=True, secondary_axis=True, secondary_label=None, linewidth=4, axes_colored=True,
    ylabel=None, xlabel=None, loc_legend='upper right', ylim_off=0.05, xlim_off=None, title=None
):
    """Plot effective modulus against porosity."""
    if dark_mode:
        text_color, face_color, edge_color = 'white', 'black', 'white'
    else:
        text_color, face_color, edge_color = 'black', 'white', 'black'

    fig, ax = plt.subplots(figsize=(12, 10), facecolor=face_color, edgecolor=edge_color)
    fig.set_facecolor(face_color)

    if axes_colored:
        ax.set_facecolor(face_color)
        for spine in ax.spines.values():
            spine.set_edgecolor('peru')
        y_color = 'peru'
    else:
        for spine in ax.spines.values():
            spine.set_edgecolor(edge_color)
        y_color = text_color

    if title is not None:
        ax.set_title(title, color=text_color)

    if types == 'all':
        types = ['voigt', 'reuss', 'avg', 'hs_upper', 'hs_lower']
    elif isinstance(types, str):
        types = [types]

    if cmap_set is None:
        cmap_val = global_settings.get('colormap', 'cm.batlow')
        cmap_set = _resolve_colormap(cmap_val)
    elif isinstance(cmap_set, str):
        cmap_set = _resolve_colormap(cmap_set)

    n_types = len(types)
    colors = [cmap_set(i/(n_types-1) if n_types > 1 else 0.5) for i in range(n_types)]

    for i, mod_type in enumerate(types):
        modulus_values = np.array(data[mod_type])
        labels = {
            'voigt': 'Voigt Bound',
            'reuss': 'Reuss Bound',
            'hs_upper': 'Hashin–Shtrikman Upper Bound',
            'hs_lower': 'Hashin–Shtrikman Lower Bound',
            'avg': 'Voigt-Reuss-Hill Average',
        }

        _marker_style = {'voigt': '-', 'reuss': '--', 'hs_upper': 'dashed', 'hs_lower': '-.', 'avg': '-'}

        ax.plot(fraction, modulus_values, label=labels[mod_type], linestyle=_marker_style[mod_type], 
                marker=marker, markersize=markersize, color=colors[i], linewidth=linewidth)

    if ylabel is not None and isinstance(ylabel, (tuple, list)) and len(ylabel) == 2:
        y1_label, y2_label = ylabel
    else:
        y1_label = ""
        y2_label = ""

    x_label_str = "Porosity" if xlabel is None else xlabel
    ax.set_xlabel(x_label_str, color=text_color)
    ax.set_ylabel(y1_label, color=y_color)

    ax.set_facecolor(face_color)
    for spine in ax.spines.values():
        spine.set_edgecolor(edge_color)

    legend = ax.legend(facecolor=face_color, edgecolor=edge_color, loc=loc_legend)
    for text in legend.get_texts():
        text.set_color(text_color)

    if grid:
        plt.grid(True, linestyle='--', alpha=0.7)

    ax.tick_params(axis='y', colors=y_color, which='both')
    ax.tick_params(axis='x', colors=text_color, which='both')
    if xlabel_percent:
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.00))

    if xlim_off is None:
        plt.xlim([0, 1])
    else:
        if isinstance(fraction, (float, int)):
            fraction = np.array([fraction])
        else:
            fraction = np.asarray(fraction).flatten()
        x_min = np.min(fraction)
        x_max = np.max(fraction)
        x_margin = xlim_off * (x_max - x_min) if x_max != x_min else xlim_off * x_max
        plt.xlim([x_min - x_margin, x_max + x_margin])

    all_values = []
    for mod_type in types:
        all_values.extend(data[mod_type])

    data_min = min(all_values) if all_values else 0
    data_max = max(all_values) if all_values else 1

    y_margin = ylim_off * (data_max - data_min) if data_max != data_min else ylim_off * data_max
    ax.set_ylim([data_min - y_margin, data_max + y_margin])

    if secondary_axis:
        ax2 = ax.twinx()
        ax2.set_facecolor(face_color)

        if axes_colored:
            for spine in ax2.spines.values():
                spine.set_edgecolor('tomato')
            y2_color = 'tomato'
        else:
            for spine in ax2.spines.values():
                spine.set_edgecolor(edge_color)
            y2_color = text_color

        secondary_min = data_min
        secondary_max = data_max
        y_margin = ylim_off * (secondary_max - secondary_min) if secondary_max != secondary_min else ylim_off * secondary_max
        ax2.set_ylim([secondary_min - y_margin, secondary_max + y_margin])

        if secondary_label:
            ax2.set_ylabel(secondary_label, color=y2_color)
        else:
            ax2.set_ylabel(y2_label, color=y2_color)

        ax2.tick_params(axis='y', colors=y2_color)
        for spine in ax2.spines.values():
            spine.set_edgecolor(edge_color)

    return fig, ax


def get_figure_colors(fig, num_colors=10, format='all', print_colors=True, data_only=True):
    """
    Extract colors used in a Matplotlib figure and convert them to RGB, CMYK, and HEX formats.
    """
    def rgb_to_cmyk(rgb):
        r, g, b = rgb[:3]
        if (r, g, b) == (0, 0, 0):
            return (0, 0, 0, 100)
        c = 1 - r
        m = 1 - g
        y = 1 - b
        k = min(c, m, y)
        if k == 1:
            return (0, 0, 0, 100)
        c = ((c - k) / (1 - k)) * 100
        m = ((m - k) / (1 - k)) * 100
        y = ((y - k) / (1 - k)) * 100
        k = k * 100
        return (c, m, y, k)

    def rgb_to_hex(rgb):
        r, g, b = rgb[:3]
        return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

    data_colors_rgba = set()
    decoration_colors_rgba = set()

    for ax in fig.get_axes():
        for patch in ax.patches:
            if hasattr(patch, 'get_facecolor'):
                data_colors_rgba.add(tuple(patch.get_facecolor()))
        for line in ax.get_lines():
            if hasattr(line, 'get_color'):
                color = line.get_color()
                if isinstance(color, str):
                    from matplotlib.colors import to_rgba
                    data_colors_rgba.add(to_rgba(color))
                else:
                    data_colors_rgba.add(tuple(color))
        for collection in ax.collections:
            if hasattr(collection, 'get_facecolors'):
                face_colors = collection.get_facecolors()
                if len(face_colors) > 0:
                    if len(face_colors) > num_colors:
                        indices = np.linspace(0, len(face_colors)-1, num_colors, dtype=int)
                        for idx in indices:
                            data_colors_rgba.add(tuple(face_colors[idx]))
                    else:
                        for color in face_colors:
                            data_colors_rgba.add(tuple(color))

        if not data_only:
            from matplotlib.colors import to_rgba
            if hasattr(ax, 'get_facecolor'):
                decoration_colors_rgba.add(tuple(to_rgba(ax.get_facecolor())))
            for spine in ax.spines.values():
                if hasattr(spine, 'get_edgecolor'):
                    decoration_colors_rgba.add(tuple(to_rgba(spine.get_edgecolor())))
            if ax.xaxis.label:
                decoration_colors_rgba.add(tuple(to_rgba(ax.xaxis.label.get_color())))
            if ax.yaxis.label:
                decoration_colors_rgba.add(tuple(to_rgba(ax.yaxis.label.get_color())))
            if ax.title:
                decoration_colors_rgba.add(tuple(to_rgba(ax.title.get_color())))
            for tick in ax.xaxis.get_major_ticks():
                if tick.label1:
                    decoration_colors_rgba.add(tuple(to_rgba(tick.label1.get_color())))
            for tick in ax.yaxis.get_major_ticks():
                if tick.label1:
                    decoration_colors_rgba.add(tuple(to_rgba(tick.label1.get_color())))

    if not data_only:
        from matplotlib.colors import to_rgba
        decoration_colors_rgba.add(tuple(to_rgba(fig.get_facecolor())))

    data_colors_rgba = sorted(list(data_colors_rgba))
    decoration_colors_rgba = sorted(list(decoration_colors_rgba))

    if len(data_colors_rgba) < num_colors:
        for ax in fig.get_axes():
            for collection in ax.collections:
                if hasattr(collection, 'get_cmap'):
                    cmap = collection.get_cmap()
                    if cmap is not None:
                        sample_colors = cmap(np.linspace(0, 1, num_colors))
                        for color in sample_colors:
                            data_colors_rgba.add(tuple(color))
                        break
        data_colors_rgba = sorted(list(data_colors_rgba))

    if len(data_colors_rgba) > num_colors:
        indices = np.linspace(0, len(data_colors_rgba)-1, num_colors, dtype=int)
        data_colors_rgba = [data_colors_rgba[i] for i in indices]

    result = {}

    if format in ['rgb', 'all']:
        result['rgb'] = {
            'data_colors': data_colors_rgba,
            'decoration_colors': decoration_colors_rgba if not data_only else []
        }

    if format in ['cmyk', 'all']:
        result['cmyk'] = {
            'data_colors': [rgb_to_cmyk(rgb) for rgb in data_colors_rgba],
            'decoration_colors': [rgb_to_cmyk(rgb) for rgb in decoration_colors_rgba] if not data_only else []
        }

    if format in ['hex', 'all']:
        result['hex'] = {
            'data_colors': [rgb_to_hex(rgb) for rgb in data_colors_rgba],
            'decoration_colors': [rgb_to_hex(rgb) for rgb in decoration_colors_rgba] if not data_only else []
        }

    if print_colors:
        print(f"\n{'='*80}")
        print(f"DATA COLORS (Colormap/Visualization): {len(data_colors_rgba)} colors extracted")
        print("=" * 80)
        for i, rgb in enumerate(data_colors_rgba, 1):
            print(f"\nData Color {i}:")
            if 'rgb' in result:
                print(f"  RGB:  ({rgb[0]:.3f}, {rgb[1]:.3f}, {rgb[2]:.3f})")
            if 'cmyk' in result:
                c, m, y, k = result['cmyk']['data_colors'][i-1]
                print(f"  CMYK: (C:{c:.1f}%, M:{m:.1f}%, Y:{y:.1f}%, K:{k:.1f}%)")
            if 'hex' in result:
                print(f"  HEX:  {result['hex']['data_colors'][i-1]}")
        if not data_only and len(decoration_colors_rgba) > 0:
            print(f"\n{'='*80}")
            print(f"DECORATION COLORS (Axes/Text/Background): {len(decoration_colors_rgba)} colors extracted")
            print("=" * 80)
            for i, rgb in enumerate(decoration_colors_rgba, 1):
                print(f"\nDecoration Color {i}:")
                if 'rgb' in result:
                    print(f"  RGB:  ({rgb[0]:.3f}, {rgb[1]:.3f}, {rgb[2]:.3f})")
                if 'cmyk' in result:
                    c, m, y, k = result['cmyk']['decoration_colors'][i-1]
                    print(f"  CMYK: (C:{c:.1f}%, M:{m:.1f}%, Y:{y:.1f}%, K:{k:.1f}%)")
                if 'hex' in result:
                    print(f"  HEX:  {result['hex']['decoration_colors'][i-1]}")
        print("=" * 80)

    return result


def save_figure(figure, filename=None, format="png", dpi=300, log=True):
    """Save a Matplotlib figure to the output directory."""
    output_path = check_output_folder()

    if filename is None:
        existing_files = glob.glob(os.path.join(output_path, "figure_*.png"))
        existing_indices = [int(os.path.basename(name).split("_")[1].split(".")[0]) for name in existing_files]
        highest_index = max(existing_indices, default=0)
        new_index = highest_index + 1
        index_formatted = f"{new_index:03d}"
        filename = os.path.join(output_path, f"figure_{index_formatted}")
    else:
        filename = os.path.join(output_path, filename)

    full_path = f"{filename}.{format}"
    figure.savefig(full_path, dpi=dpi)

    if log:
        print(f"Figure saved at: {os.path.abspath(full_path)}")
