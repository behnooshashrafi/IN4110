# Assignment 2: Implementation of Array
First we check if the given other is number of array of something else entirely in which case we raise a TypeError. This is done for all of functions with the input other.
## __init__
takes the shape and unpacked values in tuple type. By value[0] the first element of the data can be accessed. Here I only check the fisrt element for being int, float or bool because later all the values are checked to be of the same type. 
Using shape[0] we access number of rows and shape[1] is the number of columns. 
I impelemented the 1D and 2D array separately for each function. Using the len(shape) == 1 or 2, we will know if our array is 1D or 2D. 
For 1D, the array is a list of values.
for 2D, the array is a list and lists.

## __ str__

For the 1D case we simply return the string version of the same list.
For 2D we add [] to the beginning and end of the array and at the end of each list (row) we add a break line so the printed array will look like matrix.

## __getitem__
returns the value of a given index. for 2D we should call array._getitem__().__getitem__()
 
## __add__/__sub__/__mul__
Again the 1D and 2D arrays are handled individually. 
First we check if the given other is number of array of something else entirely in which case we raise a TypeError. This is done for all of functions with the input other.
The float and int are handled separatly, then we raise a NotImplemented error for boolean, and then the array case is divided into 1D and 2D case.
after adding/sunbtracting/multiplying the resulting list will be converted to a type Array.

## __radd__/__rsub__/__rmul__
All of these cases are handed to __add__/__sub__/__mul__ respectively, using the other input. For __rsub__ the result is multiplied by -1:
b-a = -a+b = -(a-b)
by calculating a-b instead of b-a we need to multiply it by -1 so it will give us the correct answer.

## __eq__/is_equal
We set the a to true and check every possibility and make it False if required. 
The same for is_equal only here we have a list in which we fill for each element. This list will be returned as an array type.

## min/mean

For min a variable is set equal to the first element of the array and then compared to the rest of the array. If the new element is smaller the variable is updated.
For mean we have a variabe = 0.0 (float).
then the sum of all the elements are taken and divided by the number of elements which is for 1D: shape[0] and for 2D: shape[0]*shape[1] or math.prod(shape).
It is set to float to prevent the compiler from rounding to an intereger.ß
