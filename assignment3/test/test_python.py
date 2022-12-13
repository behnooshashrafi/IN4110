from instapy.python_filters import python_color2gray, python_color2sepia
import numpy as np
import pytest

def test_color2gray(image):
    # run color2gray
    gray_image= python_color2gray(image)
    # check that the result has the right shape, type
    assert len(gray_image.shape) == 2
    assert gray_image.dtype == 'uint8'
    # assert uniform r,g,b values
    np.random.seed(1)
    # expected random pixel value
    H = gray_image.shape[0]
    W = gray_image.shape[1]
    for n in range(5):
        i = np.random.randint(H)
        j = np.random.randint(W)
        expected_value = image[i, j, :] @ np.array([0.21, 0.72, 0.07])
        assert gray_image[i,j] == int(expected_value)

    


def test_color2sepia(image):
    # run color2sepia
    sepia_image= python_color2sepia(image)
    # check that the result has the right shape, type
    assert len(sepia_image.shape) == 3
    assert sepia_image.dtype == 'uint8'
    # verify some individual pixel samples
    # according to the sepia matrix
    sepia_matrix = np.array([
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131],
    ])
    # expected random pixel value
    H = sepia_image.shape[0]
    W = sepia_image.shape[1]
    for i in range(5):
        i = np.random.randint(H)
        j = np.random.randint(W)
        expected_value = image[i,j,:].dot(sepia_matrix.T)
        expected_value[np.where(expected_value > 255)] = 255
        expected_value=expected_value.astype("uint8")
        assert np.array_equal(sepia_image[i,j,:],expected_value)
