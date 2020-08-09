"""
Random, Recursive Art Generator
@author: Andrea Lindner
"""

import math
import random
from PIL import Image


def build_random_function(min_depth, max_depth):
    """
    Builds a random function of depth at least min_depth and depth at most
    max_depth. 
    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
    Returns:
        The randomly generated function represented as a nested list.
        (See the assignment writ-eup for details on the representation of these functions)
    """

    if max_depth == 1:
        return [random.choice(["x","y"]),(min_depth - 1, max_depth - 1), (min_depth-1, max_depth-1)]
    if min_depth <= 1:
        return [random.choice(["x", "y","avg","prod","sin", "cos"]), build_random_function(min_depth -1, max_depth - 1), build_random_function(min_depth-1, max_depth-1)]
    else:
        return [random.choice(["avg","prod","sin", "cos"]), build_random_function(min_depth -1, max_depth - 1), build_random_function(min_depth-1, max_depth-1)]


def evaluate_random_function(f, x, y):
    """
    Evaluate the random function f with inputs x,y.
    Args:
        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
    Returns:
        The function value
    """

    if f[0] == "x":
       return x
    if f[0] =="y":
       return y
    if f[0] == "prod":
        return evaluate_random_function(f[1],x,y)* evaluate_random_function(f[2],x,y)
    if f[0] == "sin":
        return math.sin(math.pi*evaluate_random_function(f[1],x,y))
    if f[0] == "cos":
        return math.cos(math.pi*evaluate_random_function(f[1],x,y))
    if f[0] == "avg":
        return .5*(evaluate_random_function(f[1],x,y) + evaluate_random_function(f[2],x,y))
    pass

def remap_interval(val,
        input_interval_start,
        input_interval_end,
        output_interval_start,
        output_interval_end):
    """
    Given an input value in the interval [input_interval_start,
    input_interval_end], returns an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].
    Args:
        val: the value to remap
        input_interval_start: the start of the interval that contains all possible values for val
        input_interval_end: the end of the interval that contains all possible values for val
        output_interval_start: the start of the interval that contains all possible output values
        output_inteval_end: the end of the interval that contains all possible output values
    Returns:
        The value remapped from the input to the output interval scaling away from the value from the start by absolute value output/input interval
    """

    result = ((val - input_interval_start) / (input_interval_end - input_interval_start))* (output_interval_end - output_interval_start) + output_interval_start
    return result

def color_map(val):
    """
    Remps input value into a color code.
    Args:
        val: value to remap, must be a float in the interval [-1, 1]
    Returns:
        An integer in the interval [0,255]
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)

def generate_art(filename, x_size=350, y_size=350):
    """
    Generate computational art and save as an image jpg file.
    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """

    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Creates image and loops over all pixels
    image_creator = Image.new("RGB", (x_size, y_size))
    pixels = image_creator.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x, y)),
                color_map(evaluate_random_function(green_function, x, y)),
                color_map(evaluate_random_function(blue_function, x, y))
            )
    image_creator.save(filename)

if __name__ == '__main__':
    generate_art("myart.png")