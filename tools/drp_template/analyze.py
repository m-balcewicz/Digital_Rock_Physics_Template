import numpy as np
from skimage.measure import label


def connected_porespace(data):
    # Initialization
    nx, ny, nz = data.shape
    image3DConnected = np.ones((nx, ny, nz), dtype=np.uint8)

    # Step 1: Labeling the pores
    # Inverse grains <-> pores
    image3DInverse = np.abs(1 - data)
    poreLabel = label(image3DInverse, connectivity=1)
    # image3DInverseLabel = poreLabel
    #
    # # Step 2: Find the label number that exist on both ends
    # tempFirstSlide = image3DInverseLabel[:, :, 0]
    # tempLastSlide = image3DInverseLabel[:, :, -1]
    #
    # labelFirstSlide = np.unique(tempFirstSlide)
    # labelLastSlide = np.unique(tempLastSlide)
    # labelEffective = np.intersect1d(labelFirstSlide, labelLastSlide)
    #
    # # Step 3: Create connected pore space
    # nLabel = len(labelEffective)
    # for i in range(nLabel):
    #     lbl = labelEffective[i]
    #     if lbl >= 1:  # Pore = 1+ -> 0
    #         image3DConnected[image3DInverseLabel == lbl] = 0
    #     else:  # Grain = 0 -> 1
    #         image3DConnected[image3DInverseLabel == lbl] = 1

    return poreLabel
