import alsaaudio
import audioop

from recursive_art import *

# FILENAME = 'volume.png'


def generate_viz(x_size=350, y_size=350):
    """ Generate computational art and save as an image file.
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(0, 3)
    green_function = build_random_function(0, 3)
    blue_function = build_random_function(0, 3)

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

    # im.save(filename)
    im.show()


if __name__ == '__main__':
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, 0)
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(160)

    while True:
        l, data = inp.read()
        if l:
            print audioop.rms(data, 2)
            generate_viz(FILENAME)
    # generate_viz(FILENAME)