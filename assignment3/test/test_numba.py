from instapy.numba_filters import numba_color2gray, numba_color2sepia
import numpy as np
import numpy.testing as nt


def test_color2gray(image, reference_gray):
    gray_image= numba_color2gray(image)
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
        
    nt.assert_allclose(gray_image, reference_gray)


def test_color2sepia(image, reference_sepia):
    sepia_image= numba_color2sepia(image)
    assert len(sepia_image.shape) == 3
    assert sepia_image.dtype == 'uint8'
    # assert uniform r,g,b values
    np.random.seed(1)
    # expected random pixel value
    sepia_matrix = np.array([
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131],
    ])
    H = sepia_image.shape[0]
    W = sepia_image.shape[1]
    for n in range(5):
        i = np.random.randint(H)
        j = np.random.randint(W)
        expected_value = image[i,j,:].dot(sepia_matrix.T)
        expected_value[np.where(expected_value > 255)] = 255
        expected_value = expected_value.astype("uint8")
        nt.assert_allclose(sepia_image[i,j,:], expected_value)
        
    nt.assert_allclose(sepia_image, reference_sepia)
