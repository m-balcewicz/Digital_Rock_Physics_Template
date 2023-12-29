import numpy as np

__all__ = [
    'check_binary',
    'list_dir_info',
    'list_dir_info'
]

from drp_template.default_params import print_style


def check_binary(model, filename):
    unique_phases = np.unique(model)

    if min(unique_phases) == 0:
        print_style(f'{filename}:\n'
                    f'Nice data; the minimum value in your data is 0'
                    )
    elif min(unique_phases) == -1:
        # print("+++ automatic adjustment is needed")
        print_style(f'{filename}:\n'
                    f'Ups, the minimum value in your data is -1. Automatic adjustments are needed.'
                    )
        # print(f"min value: {min(unique_phases)}")
        model = model + 1
    elif min(unique_phases) == 1:
        # print("+++ automatic adjustment is needed")
        print_style(f'{filename}: \n'
                    f'Ups, the minimum value in your data is 1. Automatic adjustments are needed.'
                    )
        # print(f"min value: {min(unique_phases)}")
        model = model - 1

    return model

def get_dir_info(directory):
    file_info_list = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_info = {}
            file_info['filename'] = filename
            file_info['filetype'] = os.path.splitext(filename)[1]
            file_info['filesize_bytes'] = os.path.getsize(file_path)
            file_info['filesize_megabytes'] = file_info['filesize_bytes'] / 1000000.0
            file_info['full_path'] = os.path.abspath(file_path)
            file_info_list.append(file_info)

    file_info_list = pd.DataFrame(file_info_list)
    return file_info_list


def list_dir_info(directory, extension=None):
    """
    List all files with a specific extension in a directory,
    or list all subfolders if no extension is provided.

    Args:
        directory (str): The directory to search for files and subfolders.
        extension (str, optional): The file extension to filter the files.
                                   Default is None.

    Returns:
        list: A list of file names with the specified extension in the directory,
              or a list of subfolder names in the directory.

    """
    directory_listing = []
    for entry in os.scandir(directory):
        if entry.is_dir():
            directory_listing.append(entry.name)

    if extension is not None:
        directory_listing = [file for file in directory_listing
                             if any(file.endswith(extension) for file in os.listdir(os.path.join(directory, file)))]

    return directory_listing