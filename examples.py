import MakeModel
from import_data import import_2d_tiff
from show_data import visualize_plane

# dir_path_raw = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics/Examples/400cube_raw'
# dir_path_segmented = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics/Examples/400cube_segmented'
# dir_path_segmented = '/Volumes/mbalcewicz/SCIENCE_WORLD/STUDIES/2022_PANG/Avizo_Segmentation/SANDSTONE/Sandstone_1_12-files/EXPORT/Sandstone_1_12_segmented.raw'
# data_raw = import_ct(dir_path_raw, 1)
# data_raw = data_raw[0]  # the imported data file is a tuple
# show_ct(data_raw, 1, 100)

# data_segmented = import_ct(dir_path_segmented, 2)
# data_segmented = data_segmented[0]  # the imported data file is a tuple
# figure = show_ct(data_segmented, 2, 100)

# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# import matplotlib.pyplot as plt
# from skimage import io
# import numpy as np

# from PIL import Image

# data = import_ct('/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics/Subvolume_320cube', 1)
# show_ct(data, 1, 100)

# path = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics/Subvolume_320cube/subvolume_320cube_0000.tif'
# my_image = io.imread("/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics/Subvolume_320cube/subvolume_320cube_0000.tif")
# print(my_image)
# random_image = np.random.random([500, 500])
# plt.imshow(random_image)
# plt.show()
# print(f'min: {random_image.min()} and max:{random_image.max()}')
# img = Image.open(path)
# print(f'importing from PIl is not a numpy image: {type(img)}')
# print(img.format)
#
# img_1 = np.array(img)
# print(f'after converting to numpy array: {type(img_1)}')


# ----- matplotlib ----- #
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
#
# img = mpimg.imread(path)
# print(type(img))
# print(img.shape)
# plt.imshow(img, cmap='gray')
# plt.colorbar()
# plt.show()

# ----- scikit-image ----- #
# from skimage import io
#
# image = io.imread(path)
# print(type(image))
# sequence = io.imread_collection('/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics/Subvolume_320cube/')
# print(type(sequence))

# ----- open cv ----- #
# import cv2
# from matplotlib import pyplot as plt
#
# img = cv2.imread(path)
# print(type(img))
# cv2.imshow("Grey Image", img)
# cv2.waitKey(0)
# # plt.imshow(img)
# plt.show()
# dirpath = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics/Subvolume_320cube'
# file_Listing = io.imread_collection(f'{dirpath}/*.tif*')
# first_image = file_Listing[0]
# rows, cols = first_image.shape
# pages = len(file_Listing)
# data_man = np.zeros((rows, cols, pages))
# for i in range(pages):
#     page = file_Listing[i]
#     data_man[:, :, i] = page
# binaries = np.unique(data_man)
# print('## RAW CT image is loaded')
# print(type(data))
# slice = data[:, :, 1]
# print(f'shape of the image: {np.shape(slice)}')
# print(f'size of the image: {np.size(slice)}')
# plt.imshow(slice, cmap='gray')
# plt.show()

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# March 2023
from MakeModel import make_model
from show_data import visualize_plane
from export_data import export_raw
from import_data import import_raw
from subvolume_data import create_subvolume
import numpy as np
from control_data import check_binary
#
dir_path_segmented = './subvolume/Sandstone_1_29_400cube.raw'
#
size = 400
data_segmented = import_raw(dir_path_segmented, size)
# phases = np.unique(data_segmented)
# print(phases)
data = check_binary(data_segmented)[0]
unique_Phases = check_binary(data_segmented)[1]

type = 2
slice = int(np.shape(data)[0] / 2)
plane = 'xy'
fig = visualize_plane(data, type, slice, plane)
# data = data_segmented
# type = 2
# slice = int(np.shape(data)[0]/2)
# show_ct(data, type, slice, 'xy')

# data_subvolume = create_subvolume(data_segmented, 400, varname)

# num_phases = 2
# # data = make_model(size, num_phases)
# figure1 = show_ct(data_segmented, 2, 350, 'xy')
# path = './data'
# varname = 'homogeneous_model_800cube'
# export_model(data, path, varname)
