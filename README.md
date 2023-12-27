# Digital Rock Physics Template

The Digital Rock Physics Template is a Python package designed to facilitate digital rock physics and rock physics analysis based on the principles outlined in "The Rock Physics Handbook: Tools for Seismic Analysis of Porous Media" by Gary Mavko, Tapan Mukerji, and Jack Dvorkin (2020), DOI: [https://10.1017/9781108333016](https://doi.org/10.1017/9781108333016). This project is not affiliated with or endorsed by "The Rock Physics Handbook" authors or Cambridge University Press.

## Overview

Digital rock physics involves the integration of computational techniques, image analysis, and rock physics models to understand and predict the physical properties of porous media. This package provides a set of tools for working with digital rock data, performing simulations, and visualizing results.

## Features

- **Digital Rock Data Handling:** Import and manipulate digital rock data.
- **Visualization:** Generate visualizations, including slices and phase fraction tables.
- **Parameter Management:** Easily update and manage model parameters.


## Installation

Follow these steps to install and use the Digital Rock Physics Template:

### 1. Clone the Repository

Clone the GitHub repository to your local machine using the following command:

```bash
git clone https://github.com/m-balcewicz/Digital_Rock_Physics_Template.git
```

### 2. Navigate to the Project Directory
Change your current working directory to the project folder:
```bash
cd Digital_Rock_Physics_Template
```

### 3. Create a Conda Virtual Environment (Optional but Recommended)

It's good practice to use a virtual environment to isolate your project's dependencies. Create a Conda virtual environment with the following command:
```bash
conda create --name drp_template python=3.8
```
Activate the virtual environment:
```bash
conda activate drp_template
```
### 4. Install Dependencies
Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

### 5. Run the package
Now you can use your package. Start by running a sample script or exploring the provided examples.

### Contribution
If you're developing or contributing to the package, you may install it in editable mode for easy updates:
```bash
pip install -e .
```
#### Upgrade Package (if needed)
If you have already cloned the repository and want to update to the latest version:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```
Remember to check the package documentation or specific usage instructions for more details.

# R O A D M A P
## Todo list
- [ ] Convert from `drp_template` and `rp_template` to `barbara`.
- [ ] Rename `barabra` to `drp`.
- [ ] Publish DRP_Template.
- [ ] 


# N O T E S
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
pcolormesh: It is used for visua