"""Cython implementation of filter functions"""

import numpy as np
cimport numpy as np
def cython_color2gray(unsigned char[:, :, :] image):
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    cdef int H = image.shape[0]
    cdef int W = image.shape[1]
    cdef np.ndarray[np.uint8_t, ndim=2] gray_image = np.empty(shape=(H, W), dtype=np.uint8)
    cdef int x,y
    for x in range(H):
        for y in range(W):
            gray_image[x][y] = 0.21*image[x][y][0] + 0.72*image[x][y][1] + 0.07*image[x][y][2] 
    return gray_image.astype("uint8")

def cython_color2sepia(unsigned char[:, :, :] image):
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    cdef int H = image.shape[0]
    cdef int W = image.shape[1]
    cdef np.ndarray[np.uint8_t, ndim=3] sepia_image = np.empty(shape=(H, W, 3), dtype=np.uint8)
    cdef double R,G,B
    cdef int x,y
    for x in range(H):
        for y in range(W):
            R = 0.393*image[x][y][0]+ 0.769*image[x][y][1]+0.189*image[x][y][2]
            G = 0.349*image[x][y][0]+ 0.686*image[x][y][1]+0.168*image[x][y][2]
            B = 0.272*image[x][y][0]+ 0.534*image[x][y][1]+0.131*image[x][y][2]
            if R > 255:
                sepia_image[x][y][0] = 255
            else:
                sepia_image[x][y][0] = R
            
            if G > 255:
                sepia_image[x][y][1] = 255
            else:
                sepia_image[x][y][1] = G
                
            if B > 255:
                sepia_image[x][y][2] = 255
            else:
                sepia_image[x][y][2] = B
                
                
    sepia_image = sepia_image.astype("uint8")
    return sepia_image
