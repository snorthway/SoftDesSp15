"""
Steph Northway
Computational Art
SoftDes Spring 2015
"""

import math
import random
from PIL import Image

FUNCTIONS = {
    'x': lambda x, y: x,
    'y': lambda x, y: y,
    'prod': lambda x, y: x * y,
    'avg': lambda x, y: 0.5 * (x + y),
    'cos_pi': lambda x: math.cos(math.pi * x),
    'sin_pi': lambda x: math.sin(math.pi * x)
}


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    depth = random.randint(min_depth, max_depth)
    # separate bottom-level functions from others
    base_funcs = ['x', 'y']
    interm_funcs = filter(lambda x: x not in base_funcs, FUNCTIONS.keys())

    def build(n):
        """
        return x or y if we're at bottom;
        otherwise return any of the other functions
        """
        if n == 0:
            return [random.choice(base_funcs)]
        else:
            f = random.choice(interm_funcs)
            # If it's sine or cosine, only takes one argument; otherwise 2
            if f.endswith('pi'):
                return [f, build(n-1)]
            else:
                return [f, build(n-1), build(n-1)]

    return build(depth)


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup
        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value
        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    # if f is a 1-element list, we've reached the bottom
    if len(f) == 1:
        return FUNCTIONS[f[0]](x, y)
    else:
        # 1 argument if sine or cosine, otherwise 2
        if f[0].endswith('pi'):
            return FUNCTIONS[f[0]](evaluate_random_function(f[1], x, y))
        else:
            return FUNCTIONS[f[0]](evaluate_random_function(f[1], x, y), evaluate_random_function(f[2], x, y))


def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].
        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval
        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(5, 2, 10, -1, 1)
        -0.25
    """
    # get ranges for input and output
    len_input_interval = float(input_interval_end - input_interval_start)
    len_output_interval = float(output_interval_end - output_interval_start)

    # if no interval or the value is not in range, return minimum of the new interval
    if len_input_interval == 0 or val <= input_interval_start:
        return output_interval_start
    # if val is greater than or equal to the upper limit, return new upper limit
    elif val >= input_interval_end:
        return output_interval_end

    # how far along the first interval is val
    percent_across = (val-input_interval_start)/len_input_interval
    # multiply that percentage by the new range and add it to the start of the range
    return percent_across * len_output_interval + output_interval_start


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.
        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]
        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(5, 10)
    green_function = build_random_function(2, 5)
    blue_function = build_random_function(0, 0)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x, y)),
                color_map(evaluate_random_function(green_function, x, y)),
                color_map(evaluate_random_function(blue_function, x, y))
                )

    im.save(filename)
    im.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    generate_art("art6.png")
