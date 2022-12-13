"""Command-line (script) interface to instapy"""

import argparse
import sys

import numpy as np
from PIL import Image

import instapy
from . import io
from . import timing


def run_filter(
    file: str,
    out_file: str = None,
    filter: str = "color2gray",
    implementation: str = "python",
    scale: int = 1,
    time: int = 0,
    k: float = 1,
) -> None:
    """Run the selected filter"""
    selected_filter = instapy.get_filter(filter,implementation)
    # load the image from a file
    image = io.read_image(file)
    if scale != 1:
        # Resize image, if needed
        resized = image.resize((image.width // 2, image.height // 2))
        image = np.asarray(resized)
    
    # task 13
    if k != 1:
        if filter != "color2sepia" or implementation != "numpy":
            raise TypeError("k is only defined for numpy implementation of sepia filter")
        else:
            filtered = selected_filter(image = image, k = k)
    
    # task 14    
    if time == 1:
        runtime = timing.time_one(selected_filter, image, calls = 3)
        print(f"Average time over 3 runs: {runtime}s")

    # Apply the filter

    filtered = selected_filter(image)
    if out_file:
        # save the file
        io.write_image(filtered, "filtered_image.jpg")
    else:
        # not asked to save, display it instead
        io.display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    filter_group = parser.add_mutually_exclusive_group()
    

    # filename is positional and required
    
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=None,
        help="The filename to apply filter to",
    )
    parser.add_argument(
        "-o",
        "--out",
        help="The output filename",
    )

    # Add required arguments

    filter_group.add_argument(
        "-g",
        "--gray",
        action = "store_const",
        const = "color2gray",
        dest="filter",
        help="Select gray filter",
    )
    filter_group.add_argument(
        "-se",
        "--sepia",
        action="store_const",
        const="color2sepia",
        dest="filter",
        help="Select sepia filter",
    )

    parser.add_argument(
        "-sc",
        "--scale", 
        action ="store_const", 
        const = "scale", 
        help="Scale factor to resize image",
    )
    parser.add_argument(
        "-i",
        "--implementation",
        choices=["python","numba","numpy","cython"],
        default="python",
        help="{python,numba,numpy,cython} The implementation",
    )
    
    parser.add_argument(
        "-k",
        "--effect",
        type = float,
        default = 1,
        help="Between 0-1 for sepia effect",
    )
    
    # task 14
    parser.add_argument(
        "-r",
        "--runtime",
        type = int,
        default = 0,
        help="runtime of the chosen method for 3 runs",
    )


    # parse arguments and call run_filter
    args = parser.parse_args()
    args_dict = vars(args)
    #exit()
    file = args_dict["file"]
    implementation = args_dict["implementation"]
    time = args_dict["runtime"]
    k = args_dict["effect"]
    filter = args.filter
    #print(filter, implementation) 
    run_filter(file, filter=filter, implementation=implementation, time = time, k = k)
    
    
    
