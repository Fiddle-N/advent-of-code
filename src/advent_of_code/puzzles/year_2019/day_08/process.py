import itertools
import collections
import timeit

import PIL.Image
import PIL.ImageColor


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def read_file():
    with open("input.txt") as f:
        return f.read().rstrip()


def process_text(text):
    return [
        [int(pixel) for pixel in layer_text] for layer_text in grouper(text, 25 * 6)
    ]


def non_zeros(picture):
    return [sum(bool(pixel) for pixel in layer) for layer in picture]


def first_opaque_colour(colours):
    for colour in colours:
        if colour != 2:
            return colour


def create_picture(picture):
    height = len(picture)
    width = len(picture[0])

    im = PIL.Image.new("1", (width, height))
    for y, row in enumerate(picture):
        for x, pixel in enumerate(row):
            colour = "white" if pixel else "black"
            im.putpixel((x, y), PIL.ImageColor.getcolor(colour, "1"))
    im.save("output.png")


def main():
    text = read_file()
    picture_layers = process_text(text)

    non_zero_pixels = non_zeros(picture_layers)
    least_zeros = max(non_zero_pixels)
    fewest_zero_layer = picture_layers[non_zero_pixels.index(least_zeros)]
    count = collections.Counter(fewest_zero_layer)
    print(f"answer 1: {count[1] * count[2]} ")

    picture_colours = list(zip(*picture_layers))
    picture_flat = [first_opaque_colour(colours) for colours in picture_colours]
    picture = list(grouper(picture_flat, 25))
    create_picture(picture)


if __name__ == "__main__":
    print(timeit.timeit(main, number=1))
