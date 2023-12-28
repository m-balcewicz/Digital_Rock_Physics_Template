.. Digital Rock Physics Template documentation master file, created by
   sphinx-quickstart on Thu Dec 28 14:21:34 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Digital Rock Physics Template's documentation!
=========================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
.. * :ref:`modindex`


Figure Functions
================

Plot Histogram
--------------

This module provides a function for plotting histograms.

.. automodule:: drp_template.image._funcs
    :members: plot_histogram
    :undoc-members:
    :show-inheritance:
    :noindex:

Plot Slices
-----------

Visualize 2D slice of 3D volumetric data using Matplotlib.

.. automodule:: drp_template.image._funcs
    :members: plot_slice
    :undoc-members:
    :show-inheritance:
    :noindex:

**Parameters:**

- **data : 3D numpy array**
  The volumetric data to be visualized.

- **paramsfile : str, optional (default='parameters.json')**
  Name of the JSON file containing plotting parameters.

- **cmap_set : Matplotlib colormap, optional (default=None)**
  The colormap to be used for the plot. If not specified, the default colormap (`batlow`) will be used.

- **slice : int, optional (default=None)**
  The index of the slice along the specified plane. If not provided, the default slice index is set to the middle slice.

- **plane : str, optional (default='xy')**
  The plane along which the slice will be visualized. Valid values are 'xy', 'yz', or 'xz'.

- **subvolume : int or float, optional (default=None)**
  Specifies a subvolume indicated in the figure.

- **labels : list of str, optional (default=None)**
  Labels for the colorbar. Can be a single string or a list.

- **title : str, optional (default=None)**
  The title of the plot.

- **voxel_size : int of floats, optional (default=None)**
  The size of the voxels along each dimension.

- **dark_mode : bool, optional (default=True)**
  If True, set a dark background; otherwise, set a light background.

**Returns:**

- **fig : Matplotlib Figure**
  The Matplotlib figure object.

- **ax : Matplotlib Axes**
  The Matplotlib axes object.

**Examples:**

```python
import numpy as np
from plot_slice import plot_slice

# Generate example data
data = np.random.rand(50, 100, 200)

# Plot XY plane slice
fig, ax = plot_slice(data, cmap_set='viridis', slice=10, plane='xy', title='XY Plane slice')
plt.show()

Notes
=====
Why pcolormesh and not imshow?
--------------------------------

Both `imshow` and `pcolormesh` are functions in Matplotlib used for creating 2D visualizations. However, there are some differences between the two:

**Grid Representation:**

- **imshow:** It is designed to display a regular grid of pixels (like an image). It assumes that the data points are regularly spaced, and it directly maps each pixel to a data point.
- **pcolormesh:** It is more general and can handle irregularly spaced data. It creates a pseudocolor plot on a 2D grid and can handle different sized bins.

**Data Interpolation:**

- **imshow:** It performs interpolation on the data to smoothly display pixel values. This can be useful for visualizing continuous functions or smooth variations in data.
- **pcolormesh:** It does not perform interpolation by default. It represents the data in a piecewise constant manner, with each quadrilateral representing a constant value.

**Handling Edges:**

- **imshow:** It extends the edges of the input array to cover the entire plotting area. This behavior may not be suitable for some applications.
- **pcolormesh:** It does not extend the edges, and it is useful when you want to precisely control the boundaries of the plotted data.

**Performance:**

- **imshow:** Generally, imshow may be more efficient for regularly spaced data and large datasets.
- **pcolormesh:** It is more flexible for irregularly spaced data, but it might have a slightly higher computational cost.

**Usage:**

- **imshow:** It is often used for displaying images or regularly sampled data, such as matrices or photographs.
- **pcolormesh:** It is used for visualizing irregularly spaced data.

The corresponding function in your codebase is `plot_slice`, which is defined in `drp_template/image/_funcs.py`.

:func:`~drp_template.image._funcs.plot_slice` function details can be found in the source code.



