"""numba-optimized filters"""
from numba import jit
import numpy as np

@jit
def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.zeros((image.shape[0], image.shape[1]))
    # iterate through the pixels, and apply the grayscale transform
    for x in range(len(image)):
        for y in range(len(image[0])):
            gray_image[x][y] = 0.21*image[x][y][0] + 0.72*image[x][y][1] + 0.07*image[x][y][2]
    gray_image = gray_image.astype("uint8")
    return gray_image

@jit
def numba_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    # Iterate through the pixels
    # applying the sepia matrix
    for x in range(len(image)):
        for y in range(len(image[0])):
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

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image


...
