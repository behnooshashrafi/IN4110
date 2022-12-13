# instapy package
It is a package that enables us to apply filters on images. Two filteres were implemented using different methods. 
Filters: color2gray, color2sepia
Implementation: python, numpy, numba, cython
### color2gray:
Applies a gray scale filter to the image. We use 0.21, 0.72, and 0.07 as weight for red, green and blue channels in each pixel respectively.

### color2sepia:
Applies a sepia filter to the image. Using the sepia matrix bellow we will adjust new values for red, green and blue channels. k is between 0-1 and will tune the sepia effect:

sepia_matrix = np.array([
        [ 0.393 + 0.607*(1-k), 0.769 - 0.769*(1-k), 0.189 - 0.189*(1-k)],
        [ 0.349 - 0.349*(1-k), 0.686 + 0.314*(1-k), 0.168 - 0.168*(1-k)],
        [ 0.272 - 0.272*(1-k), 0.534 - 0.534*(1-k), 0.131 + 0.869*(1-k)],
    ])
    
    
## Implementation:
There are four different implementation for these filters. 1. pure python, 2. numpy, 3. numba, 4. cython
We timed these differnet implementations.
python is slowest because in the background of compiling python, all possible senarios are checked in if tests.
numpy is the fastest because it is written in C in the background.
numba and cython are in between. cython is python but with C, meaning some parts can be implemented faster using C programming. 
numba runs the code once and goes through all the checks and ifs once, then uses that information to run the rest. It does not check everything everytime like python does.
Speedwise in this case, for gray filter cython is faster and in sepia filter numba runs a bit faster.

## cli
All the information can be taken from the command line interface. 
The user can run in terminal using instapy following by required and optional arguments:

instapy -f:str(file address) -se/-g -i:str(implementation) -r:runtime(1:yes/0:no) -k:(sepia filter effect)

example: 

instapy -f="rain.jpg" -se -i="numpy" -r=1 -k=0

runnign: 

instapy -h

will give the user a manual for the inputs.
instapy takes the following arguments, the values is front of : are the default values.

{'file': 'rain.jpg', 'out': None, 'filter': 'color2sepia', 'scale': None, 'implementation': 'numpy', 'effect': 1, 'runtime': 0}

## Instalation:
cd into root directory (assignment3 in this case)

$ pip install --editable .

Install Package:

$ pip install .

Image filtering:

pip install numpy pillow line-profiler

### test:
install pytest:

python3 -m pytest -v test/test_package.py

test:

$ pytest

