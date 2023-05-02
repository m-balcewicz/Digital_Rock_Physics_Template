import os
import pandas as pd


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome')
    print('developed 05/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


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


# ------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()
