"""
Array class for assignment 2
"""
import math
class Array:

    def __init__(self, shape, *values):
        """Initialize an array of 1-dimensionality. Elements can only be of type:

        - int
        - float
        - bool

        Make sure the values and shape are of the correct type.

        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either int, float or boolean.

        Raises:
            TypeError: If "shape" or "values" are of the wrong type.
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """

        # Check if the values are of valid types
        if not isinstance(values[0], (int,float,bool)):
            raise TypeError("Values are the wrong type: int, float, bool.")

        # Check that the amount of values corresponds to the shape
            
        if not isinstance(shape, tuple):#checking that the input shape is tuple
            raise TypeError("Shape is not a tuple.")
            
        for i in values:# checking that all values are the same type
            if type(i) != type(values[0]):
                raise ValueError("Values are not all the same type.")
        
        # Set class-variables
        
        self.shape = shape
        
        if len(shape) == 1: #1D case
            if len(values) != shape[0]: # checking that the value is correspinding to the shape
                raise ValueError("Values do not fit the shape.")
    
            self.array = list(values)
            
        elif len(shape) == 2: #2D case
            if len(values) != math.prod(shape):
                raise ValueError("Values do not fit the shape.")
                
            self.array = []
            for i in range(shape[0]):# checking that the value is correspinding to the shape
                temp = list(values[i*shape[1]:(i+1)*shape[1]]) 
                self.array.append(temp) # appending each. row as a temp list 
        else:
            raise TypeError("Shape is 3D or more. NotImplemented")
        

    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """
        if len(self.shape) == 1:
            a = str(self.array)
        else:
            a = "["
            for i in range(self.shape[0]):
                a += str(self.array[i])
                if (i != self.shape[0] - 1):
                    a += str(",\n")
            a += "]"
        return a

                
    def __getitem__(self, index):

        return self.array[index]

    def __add__(self, other):
        
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """

        # check that the method supports the given arguments (check for data type and shape of array)
        # if the array is a boolean you should return NotImplemented
        a = []
        if isinstance(other, (float, int, bool, Array)):
            if isinstance(other, (float,int)):
                if len(self.shape) == 1:
                    if not isinstance(other, type(self.array[0])):
                        raise TypeError("The value and array have different types")
                    else:
                        for i in range(len(self.array)):
                            a.append(self.array[i] + other)
                else:
                    if not isinstance(other, type(self.array[0][0])):
                        raise TypeError("The value and array have different types")
                    else:
                        for i in range(self.shape[0]):
                            for j in range(self.shape[1]):
                                a.append(self.array[i][j] + other)

            elif isinstance(other, bool):
                raise Error("NotImplemented")

            elif len(self.shape) == 1:    
                if type(other[0]) != type(self.array[0]):
                    raise ValueError("Arrays not the same type")

                if other.shape[0] != self.shape[0]:
                    raise ValueError("Arrays not the same shape")

                for index in range(self.shape[0]):
                    a.append(self.array[index] + other[index]) 
            else:

                if not isinstance(other.__getitem__(0).__getitem__(0), type(self.array[0][0])): 
                    raise ValueError("Arrays not the same type")

                if other.shape != self.shape:
                    raise ValueError("Arrays not the same shape")   

                for i in range(self.shape[0]):
                    for j in  range(self.shape[1]):
                        a.append(self.array[i][j] + other[i][j])
        else:
            raise TypeError("Not number or array")
        add_result = Array(self.shape,*a)
        
        return add_result
    

    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        return self.__add__(other)

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        a = []
        if isinstance(other, (float, int, bool, Array)):
            if isinstance(other, (float,int)):
                if len(self.shape) == 1:
                    if not isinstance(other, type(self.array[0])):
                        raise TypeError("The value and array have different types")
                    else:
                        for i in range(len(self.array)):
                            a.append(self.array[i] - other)
                else:
                    if not isinstance(other, type(self.array[0][0])):
                        raise TypeError("The value and array have different types")
                    else:
                        for i in range(self.shape[0]):
                            for j in range(self.shape[1]):
                                a.append(self.array[i][j] - other)

            elif isinstance(other, bool):
                raise Error("NotImplemented")

            elif len(self.shape) == 1:    
                if type(other[0]) != type(self.array[0]):
                    raise ValueError("Arrays not the same type")

                if other.shape[0] != self.shape[0]:
                    raise ValueError("Arrays not the same shape")

                for index in range(self.shape[0]):
                    a.append(self.array[index] - other[index]) 
            else:

                if not isinstance(other.__getitem__(0).__getitem__(0), type(self.array[0][0])): 
                    raise ValueError("Arrays not the same type")

                if other.shape != self.shape:
                    raise ValueError("Arrays not the same shape")   

                for i in range(self.shape[0]):
                    for j in  range(self.shape[1]):
                        a.append(self.array[i][j] - other[i][j])
        else:
            raise TypeError("Not number or array")

        sub_result = Array(self.shape,*a)
        return sub_result
        

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        return self.__sub__(other).__mul__(-1)

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        a = []
        if isinstance(other, (float, int, bool, Array)):
            if isinstance(other, (float,int)):
                if len(self.shape) == 1:
                    if not isinstance(other, type(self.array[0])):
                        raise TypeError("The value and array have different types")
                    else:
                        for i in range(len(self.array)):
                            a.append(self.array[i] * other)
                else:
                    if not isinstance(other, type(self.array[0][0])):
                        raise TypeError("The value and array have different types")
                    else:
                        for i in range(self.shape[0]):
                            for j in range(self.shape[1]):
                                a.append(self.array[i][j] * other)

            elif isinstance(other, bool):
                raise Error("NotImplemented")

            elif len(self.shape) == 1:    
                if type(other[0]) != type(self.array[0]):
                    raise ValueError("Arrays not the same type")

                if other.shape[0] != self.shape[0]:
                    raise ValueError("Arrays not the same shape")

                for index in range(self.shape[0]):
                    a.append(self.array[index] * other[index]) 
            else:

                if not isinstance(other.__getitem__(0).__getitem__(0), type(self.array[0][0])): 
                    raise ValueError("Arrays not the same type")

                if other.shape != self.shape:
                    raise ValueError("Arrays not the same shape")   

                for i in range(self.shape[0]):
                    for j in  range(self.shape[1]):
                        a.append(self.array[i][j] * other[i][j])
        else:
            raise TypeError("Not number or array")
        mul_result = Array(self.shape,*a)
        
        return mul_result

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        # Hint: this solution/logic applies for all r-methods
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        
        a = True
        if isinstance(other, (float,int,bool)):
            a = False
        if isinstance(other, Array):
            if len(self.shape) == 1:    
                if type(other[0]) != type(self.array[0]):
                    a = False
                    raise ValueError("Arrays not the same type")

                if other.shape[0] != self.shape[0]:
                    a = False
                    raise ValueError("Arrays not the same shape")

                for index in range(self.shape[0]):
                    if not other[index] == self.array[index]:
                        a = False
            else:

                if not isinstance(other.__getitem__(0).__getitem__(0), type(self.array[0][0])): 
                    a = False
                    raise ValueError("Arrays not the same type")

                if other.shape != self.shape:
                    a = False
                    raise ValueError("Arrays not the same shape")   

                for i in range(self.shape[0]):
                    for j in  range(self.shape[1]):
                        if not self.array[i][j] == other[i][j]:
                            a = False
        return a
        

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """

        a = []
        if isinstance(other, (float, int, bool, Array)):
            if isinstance(other, (float,int)):
                if len(self.shape) == 1:
                    if not isinstance(other, type(self.array[0])):
                        raise TypeError("The value and array have different types")
                    else:
                        for i in range(len(self.array)):
                            if self.array[i] == other:
                                a.append(True)
                            else:
                                a.append(False)
                else:
                    if not isinstance(other, type(self.array[0][0])):
                        raise TypeError("The value and array have different types")
                    else:
                        for i in range(self.shape[0]):
                            for j in range(self.shape[1]):
                                if self.array[i][j] == other:
                                    a.append(True)
                                else:
                                    a.append(False)

            elif isinstance(other, bool):
                raise Error("NotImplemented")


            elif len(self.shape) == 1:    
                if type(other[0]) != type(self.array[0]):
                    raise ValueError("Arrays not the same type")

                if other.shape[0] != self.shape[0]:
                    raise ValueError("Arrays not the same shape")

                for index in range(self.shape[0]):
                    if self.array[index] == other[index]:
                        a.append(True)
                    else:
                        a.append(False)
            else:

                if not isinstance(other.__getitem__(0).__getitem__(0), type(self.array[0][0])): 
                    raise ValueError("Arrays not the same type")

                if other.shape != self.shape:
                    raise ValueError("Arrays not the same shape")   

                for i in range(self.shape[0]):
                    for j in  range(self.shape[1]):
                        if self.array[i][j] == other[i][j]:
                            a.append(True)
                        else:
                            a.append(False)
        else:
            raise TypeError("Not number or array")
        isequal = Array(self.shape,*a)
        return isequal

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """

        if len(self.shape) == 1:
            a = self.array[0]
            if isinstance(a, bool):
                raise TypeError("NotImplemented for boolean")
            else:
                for i in range(1,self.shape[0]):
                    if self.array[i] < a:
                        a = self.array[i]
        else:
            a = self.array[0][0]
            if isinstance(a, bool):
                raise TypeError("NotImplemented for boolean")
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    if self.array[i][j] < a:
                        a = self.array[i][j]
        return a

    def mean_element(self):
        """Returns the mean value of an array

        Only needs to work for type int and float (not boolean).

        Returns:
            float: the mean value
        """

        mean = 0.0
        if len(self.shape) == 1:
            
            if isinstance(self.array[0], bool):
                raise TypeError("NotImplemented for boolean")
            else:
                mean = float((sum(self.array))/self.shape[0])
        else:
            if isinstance(self.array[0][0], bool):
                raise TypeError("NotImplemented for boolean")
            for i in range(self.shape[0]):
                mean += sum(self.array[i])
            mean = float(mean/math.prod(self.shape))

        return mean


