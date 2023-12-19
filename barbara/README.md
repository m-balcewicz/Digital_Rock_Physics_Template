# Digital Rock Physics tool (Project name: barbara)

## Global settings
Since 24.11.2023 the general shape for all models is set to (x, y, z)


## Why pcolormesh and not imshow?
Both imshow and pcolormesh are functions in Matplotlib used for creating 2D visualizations. However, there are some differences between the two:

Grid Representation:

imshow: It is designed to display a regular grid of pixels (like an image). It assumes that the data points are regularly spaced, and it directly maps each pixel to a data point.
pcolormesh: It is more general and can handle irregularly spaced data. It creates a pseudocolor plot on a 2D grid and can handle different sized bins.
Data Interpolation:

imshow: It performs interpolation on the data to smoothly display pixel values. This can be useful for visualizing continuous functions or smooth variations in data.
pcolormesh: It does not perform interpolation by default. It represents the data in a piecewise constant manner, with each quadrilateral representing a constant value.
Handling Edges:

imshow: It extends the edges of the input array to cover the entire plotting area. This behavior may not be suitable for some applications.
pcolormesh: It does not extend the edges, and it is useful when you want to precisely control the boundaries of the plotted data.
Performance:

imshow: Generally, imshow may be more efficient for regularly spaced data and large datasets.
pcolormesh: It is more flexible for irregularly spaced data, but it might have a slightly higher computational cost.
Usage:

imshow: It is often used for displaying images or regularly sampled data, such as matrices or photographs.
pcolormesh: It is used for visualizing data that is represented on an unstructured grid or irregular mesh.