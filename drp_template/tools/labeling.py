import numpy as np
import matplotlib.pyplot as plt
from drp_template.default_params import update_parameters_file

__all__ = [
    'find_slice_with_all_values',
    'label_binary',
    'reorder_labels',
]


def find_slice_with_all_values(data):
    """Find xy/yz/xz slice indices that contain all unique values present in the 3D array."""
    unique_values = np.unique(data)

    def check_slice(arr2d):
        slice_unique_values = np.unique(arr2d)
        return np.all(np.isin(unique_values, slice_unique_values))

    result = {"xy": None, "yz": None, "xz": None}
    for i in range(data.shape[2]):
        if check_slice(data[:, :, i]):
            result["xy"] = i
            break
    for i in range(data.shape[0]):
        if check_slice(data[i, :, :]):
            result["yz"] = i
            break
    for i in range(data.shape[1]):
        if check_slice(data[:, i, :]):
            result["xz"] = i
            break
    return result


def label_binary(data, paramsfile='parameters.json'):
    """Interactively label binary phases using slice visualization in a notebook."""
    from IPython.display import display
    from drp_template.image import ortho_slice

    if not np.issubdtype(data.dtype, np.integer):
        raise ValueError("Input data must be a binary/segmented integer array.")

    unique = np.unique(data)
    labels = {}
    slice_index = find_slice_with_all_values(data)['xy']

    for m, value in enumerate(unique):
        data_temp = np.zeros_like(data)
        data_temp[data == value] = 1
        cmap_reds = plt.cm.Reds
        fig, ax, pcm = ortho_slice(data=data_temp, plane='xy', cmap_set=cmap_reds, paramsfile=paramsfile, title=f"Phase: {m}", slice=slice_index)
        display(fig)
        phase_name = input(f'Name the presented phase {value} with index {m}: ')
        labels[str(value)] = phase_name
        plt.close(fig)

    update_parameters_file(paramsfile, labels=labels)
    return labels


def reorder_labels(data, labels, paramsfile='parameters.json'):
    """Reorder labels of a segmented image to a consistent convention, updating params file."""
    old_order = list(labels.keys())
    set_order = list(set(labels.keys()))
    label_mapping = {old: new for new, old in zip(set_order, old_order)}
    new_labels = {new: labels[old] for old, new in label_mapping.items()}
    map_labels = np.vectorize(label_mapping.get)
    data = map_labels(data)
    update_parameters_file(paramsfile, labels=new_labels)
    return data, new_labels
