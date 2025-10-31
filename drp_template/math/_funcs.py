import numpy as np
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import warnings

# from skimage.measure import label
from drp_template.default_params import read_parameters_file, check_output_folder, update_parameters_file
from drp_template.image import ortho_slice
from drp_template.tools import find_slice_with_all_values

__all__ = [
    'get_connected_porosity',
    'get_phase_fractions',
    'label_binary',
    'reorder_labels'
]


def get_connected_porosity(data, paramsfile='parameters.json'):
    # # Initialization
    # nx = read_parameters_file(paramsfile=paramsfile, paramsvars='nx')
    # ny = read_parameters_file(paramsfile=paramsfile, paramsvars='ny')
    # nz = read_parameters_file(paramsfile=paramsfile, paramsvars='nz')

    # image3DConnected = np.ones((nx, ny, nz), dtype=np.uint8)

    # # Step 1: Labeling the pores
    # # Inverse grains <-> pores
    # image3DInverse = np.abs(1 - data)
    # poreLabel = label(image3DInverse, connectivity=1)

    # print(poreLabel)
    # # image3DInverseLabel = poreLabel
    # #
    # # # Step 2: Find the label number that exist on both ends
    # # tempFirstSlide = image3DInverseLabel[:, :, 0]
    # # tempLastSlide = image3DInverseLabel[:, :, -1]
    # #
    # # labelFirstSlide = np.unique(tempFirstSlide)
    # # labelLastSlide = np.unique(tempLastSlide)
    # # labelEffective = np.intersect1d(labelFirstSlide, labelLastSlide)
    # #
    # # # Step 3: Create connected pore space
    # # nLabel = len(labelEffective)
    # # for i in range(nLabel):
    # #     lbl = labelEffective[i]
    # #     if lbl >= 1:  # Pore = 1+ -> 0
    # #         image3DConnected[image3DInverseLabel == lbl] = 0
    # #     else:  # Grain = 0 -> 1
    # #         image3DConnected[image3DInverseLabel == lbl] = 1

    return print('this function is not implemented yet')


def get_phase_fractions(data, labels=None, paramsfile='parameters.json', log=False):
    """
    Calculate detailed phase fractions and generate a formatted table.
    
    This is the PRIMARY FUNCTION for detailed phase analysis of segmented data.
    It provides comprehensive statistics with DataFrame formatting, footer totals,
    and automatic saving to the parameters file.
    
    For quick file overview without loading data, use drp_template.tools.get_model_properties().

    Parameters:
    -----------
    data : numpy.ndarray
        The input data array (already loaded) for which fractions need to be calculated.
    labels : dict, optional (default=None)
        Dictionary mapping phase values to phase names. Keys can be strings or integers.
        Example: {"0": "Pore", "1": "Quartz", "2": "Feldspar"}
        The function handles flexible key formats (int, str) automatically.
    paramsfile : str, optional (default='parameters.json')
        Name of the JSON file where fractions will be saved.
    log : bool, optional (default=False)
        If True, print the formatted table to console.

    Returns:
    --------
    str
        A formatted table string containing phases, counts, fractions, and labels.
        Includes a footer row with totals.

    Raises:
    ------
    ValueError
        If labels is provided but is not a dictionary.

    Examples:
    ---------
    ```python
    import drp_template.input_output as io
    import drp_template.math as drp_math
    
    # Load data
    data = io.import_model('model.raw', dtype='uint8', 
                          dimensions={'nx': 400, 'ny': 400, 'nz': 400})
    
    # Basic usage without labels
    table = drp_math.get_phase_fractions(data, log=True)
    
    # With labels for better readability
    labels = {"0": "Pore", "1": "Quartz", "2": "Feldspar"}
    table = drp_math.get_phase_fractions(data, labels=labels, log=True)
    
    # Save to custom parameters file
    table = drp_math.get_phase_fractions(data, labels=labels, 
                                         paramsfile='my_model.json', log=True)
    ```
    
    Output Format:
    --------------
    The returned table includes:
    - Phase: Integer phase value
    - Count: Number of voxels for each phase
    - Fraction: Percentage of total voxels (4 decimal places)
    - Name: Phase name (if labels provided)
    - Footer: Total counts and percentages
    
    Notes:
    ------
    - This function automatically saves phase fractions to the parameters file
    - Uses pandas DataFrame for professional table formatting
    - Handles flexible label key formats (tries int, str conversions automatically)
    - Includes a footer row showing totals for validation
    - Fractions are saved using phase names as keys (if labels provided)
    
    See Also:
    ---------
    drp_template.tools.get_model_properties : Quick file overview without loading data
    """
    if labels is not None:
        if not isinstance(labels, dict):
            raise ValueError("The 'labels' argument should be a dictionary.")

    # Get the unique values and their counts
    unique_values, value_counts = np.unique(data, return_counts=True)

    # Calculate the percentage for each occurrence
    total = np.sum(value_counts)
    percentages = value_counts / total * 100

    # Combine the arrays into a single array
    table_values = np.column_stack((unique_values, value_counts, percentages))

    # Define the headers for the table
    headers = ["Phase", "Count", "Fraction"]

    # Create a DataFrame
    df = pd.DataFrame(table_values, columns=headers)

    # UPDATE
    # 25.04.2025
    # Implementing the strings for the labels correctly
    # Add the "Name" column with labels
    # if labels is not None:
    #     df["Name"] = [labels.get(phase, "") for phase in df["Phase"]]
        # Add the "Name" column with labels
    if labels is not None:
        # Try different key formats (int, str) to find matches in the labels dictionary
        df["Name"] = ["" for _ in range(len(df))]
        for i, phase in enumerate(df["Phase"]):
            phase_val = phase
            # Try different formats for the key lookup
            for key_format in [phase_val, int(phase_val), str(phase_val), str(int(phase_val))]:
                if key_format in labels:
                    df.at[i, "Name"] = labels[key_format]
                    break

    # Format the columns
    df["Phase"] = df["Phase"].astype(int).astype(str)
    df["Count"] = df["Count"].astype(int).astype(str)
    df["Fraction"] = df["Fraction"].apply(lambda x: f"{x:.4f}")

    # Add the footer row to the DataFrame
    footer = [len(unique_values), np.sum(value_counts), np.sum(percentages)]
    if labels is not None:
        footer.append("")
    df_footer = pd.DataFrame([footer], columns=headers + (["Name"] if labels is not None else []))

    # Concatenate the DataFrame and footer
    df_table = pd.concat([df, df_footer], ignore_index=True)

    # Convert the DataFrame to a string format
    table = df_table.to_string(index=False)
    
    # Update the parameters file with the fractions
    # fractions = {labels[int(phase)]: fraction for phase, fraction in zip(unique_values, percentages)}
    fractions = {labels[str(int(phase))]: fraction for phase, fraction in zip(unique_values, percentages)}
    update_parameters_file(paramsfile, fractions=fractions)

    if log:
        print(table)

    return table


def label_binary(data, paramsfile='parameters.json'):
    """
    DEPRECATED: This function has been moved to drp_template.tools.label_binary
    
    Label binary phases in a 3D volume based on user input.

    Parameters:
    -----------
    data : numpy.ndarray
        3D binary volume to be labeled.
    paramsfile : str, optional (default='parameters.json')
        Name of the JSON file containing plotting parameters.

    Returns:
    --------
    labels : dict
        Dictionary mapping phase values to user-defined labels.
        
    Notes:
    ------
    **DEPRECATION WARNING**: 
    This function has been moved from `drp_template.math.label_binary` 
    to `drp_template.tools.label_binary` for better organization.
    
    Please update your imports to:
    ```python
    from drp_template.tools import label_binary
    # or
    import drp_template.tools as tools
    labels = tools.label_binary(data, paramsfile)
    ```
    
    This wrapper will be removed in a future version.
    """
    warnings.warn(
        "label_binary has been moved from drp_template.math to drp_template.tools. "
        "Please update your imports: 'from drp_template.tools import label_binary'. "
        "This backward compatibility wrapper will be removed in a future version.",
        DeprecationWarning,
        stacklevel=2
    )
    
    # Import and call the new location
    from drp_template.tools import label_binary as _label_binary_new
    return _label_binary_new(data, paramsfile)


def reorder_labels(data, labels, paramsfile = 'parameters.json'):
    """This is a function to reorder the labels of a segmented image. The standard order for segmented images is:
    0: Pore
    1: Matrix-1 (e.g., Quartz)
    2: Matrix-2 (e.g., Feldspar)
    3: Matrix-3 (e.g., Mica)

    Args:
        data (np.ndarray): The segmented image data.
        labels (Dict[int, str]): The labels of the segmented image.
        set_order (List[int], optional): The desired order of the labels. Defaults to [1,0,2].
        paramsfile (str, optional): The parameters file to update with the new labels. Defaults to 'parameters.json'.
    """
    # Get the current order of the labels dictionary
    old_labels = list(labels.values())
    print(f"old labels: {old_labels}")
    
    # Get the current order of the labels integers
    old_order = list(labels.keys())
    print(f"old order: {old_order}")
    
    # Get the set_order from the users labels input
    set_order = list(set(labels.keys()))
    print(f"set order: {set_order}")
    
   # Create a mapping from old_order to set_order
    label_mapping = {old: new for new, old in zip(set_order, old_order)}
    print(f"label mapping: {label_mapping}")
    
    # Create a new labels dictionary with the new order
    new_labels = {new: labels[old] for old, new in label_mapping.items()}
    print(f"new labels: {new_labels}")
    
    # Create a function that maps old labels to new labels
    map_labels = np.vectorize(label_mapping.get)
    
    # Apply the function to the data array
    data = map_labels(data)
    
    # update the parameters file with the new labels
    update_parameters_file(paramsfile, labels=new_labels)
    
    return data, new_labels


