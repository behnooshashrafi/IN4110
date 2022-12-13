"""
Tests for our array class
"""

from array_class import Array

# 1D tests (Task 4)


def test_str_1d():
    assert Array((3,), 1,2,3).__str__() == '[1, 2, 3]'


def test_add_1d():
    assert (Array((3,), 1,2,3) + Array((3,), 1,1,1)).__str__() == '[2, 3, 4]'


def test_sub_1d():
    assert (Array((3,), 1,2,3) - Array((3,), 1,1,1)).__str__() == '[0, 1, 2]'


def test_mul_1d():
    assert (Array((3,), 1,2,3) * Array((3,), 2,2,2)).__str__() == '[2, 4, 6]'


def test_eq_1d():
    assert Array((3,), 2,2,2).__eq__(Array((3,), 2,2,3)) == False


def test_same_1d():
    assert (Array((3,), 2,2,2).is_equal(Array((3,), 2,4,2))).__str__() == '[True, False, True]'


def test_smallest_1d():
    assert Array((3,), 3,2,1).min_element() == 1


def test_mean_1d():
    assert Array((3,), 3,2,1).mean_element() == 2.0


# 2D tests (Task 6)


def test_add_2d():
    assert (Array((2,2), 2,4,6,8) + Array((2,2), 1,1,1,1)).__str__() == '[[3, 5],\n[7, 9]]'


def test_mult_2d():
    (Array((2,2), 2,4,6,8) * Array((2,2), 2,2,2,2)).__str__() == '[[4, 8],\n[12, 16]]'


def test_same_2d():
    assert (Array((2,2), 2,4,6,8).is_equal(6)).__str__() == '[[False, False],\n[True, False]]'


def test_mean_2d():
    assert Array((3,4), 1,2,3,4,5,6,7,8,9,10,11,12).mean_element() == 6.5


if __name__ == "__main__":
    """
    Note: Write "pytest" in terminal in the same folder as this file is in to run all tests
    (or run them manually by running this file).
    Make sure to have pytest installed (pip install pytest, or install anaconda).
    """

    # Task 4: 1d tests
    test_str_1d()
    test_add_1d()
    test_sub_1d()
    test_mul_1d()
    test_eq_1d()
    test_mean_1d()
    test_same_1d()
    test_smallest_1d()

    # Task 6: 2d tests
    test_add_2d()
    test_mult_2d()
    test_same_2d()
    test_mean_2d()


