"""
Model utility functions for Digital Rock Physics Template.
"""
import numpy as np
import os

__all__ = [
    'reshape',
    'get_dim',
    'subvolume',
]

def get_dim(dimensions_dict):
    """
    Extracts and validates model dimensions from a dictionary.
    Example: dimensions_dict = {'nz': 100, 'ny': 200, 'nx': 300}
    Returns: n1, n2, n3 (tuples of (key, value))
    """
    if dimensions_dict is None:
        raise ValueError("At least two dimensions (nx, ny, nz) must be provided.")
    nx = dimensions_dict.get('nx', None)
    ny = dimensions_dict.get('ny', None)
    nz = dimensions_dict.get('nz', None)
    if sum(dim is not None for dim in [nx, ny, nz]) < 2:
        raise ValueError("At least two dimensions (nx, ny, nz) must be provided.")
    iterator = iter(dimensions_dict.items())
    n1 = next(iterator)
    n2 = next(iterator)
    n3 = next(iterator)
    return n1, n2, n3

def reshape(model, n1, n2, n3):
    """
    Reorders axes of a model array to (nx, ny, nz) if needed.
    """
    if (n1[0], n2[0], n3[0]) != ('nx', 'ny', 'nz'):
        print("Reshaping data to the desired order (nx, ny, nz)...")
        if (n1[0], n2[0], n3[0]) == ('nx', 'nz', 'ny'):
            model_reshaped = np.moveaxis(model, (0, 1, 2), (0, 2, 1))
        elif (n1[0], n2[0], n3[0]) == ('nz', 'ny', 'nx'):
            model_reshaped = np.moveaxis(model, (0, 1, 2), (2, 1, 0))
        elif (n1[0], n2[0], n3[0]) == ('nz', 'nx', 'ny'):
            model_reshaped = np.moveaxis(model, (0, 1, 2), (2, 0, 1))
        elif (n1[0], n2[0], n3[0]) == ('ny', 'nx', 'nz'):
            model_reshaped = np.moveaxis(model, (0, 1, 2), (1, 0, 2))
        elif (n1[0], n2[0], n3[0]) == ('ny', 'nz', 'nx'):
            model_reshaped = np.moveaxis(model, (0, 1, 2), (1, 2, 0))
        else:
            raise ValueError("Unsupported shape. Unable to determine correct axis order.")
    else:
        print("Model dimensions are already in the desired order (nx, ny, nz).")
        model_reshaped = model
    return model_reshaped

def subvolume(data, set_subvolume, name_subvolume, voxel_size, directory=None, dtype='uint8', order='C'):
    """
    Creates a subvolume from the given data and saves it as a binary file.
    The subvolume is centered and has shape (set_subvolume, set_subvolume, set_subvolume).
    """
    x, y, z = data.shape
    cut_x = (x - set_subvolume) // 2
    cut_y = (y - set_subvolume) // 2
    cut_z = (z - set_subvolume) // 2
    data_subvolume = data[cut_x:x - cut_x, cut_y:y - cut_y, cut_z:z - cut_z]
    varname = f"{name_subvolume}_{set_subvolume}cube"
    if directory is None:
        from drp_template.default_params import check_output_folder
        directory = check_output_folder()
    file_path = os.path.join(directory, varname)
    import drp_template.input_output as in_out
    in_out.export_model(filename=file_path, data=data_subvolume, voxel_size=voxel_size, dtype=dtype, order=order)
    return data_subvolume
