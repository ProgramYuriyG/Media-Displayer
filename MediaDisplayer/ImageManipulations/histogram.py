import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

'''
Visually display the greyscale intensity or color channel values of a given image
'''


def display_histogram(img):
    x = np.arange(0, 256)
    width, height = img.size

    if img.mode == 'L':
        y = np.zeros(256, np.uint64)

        for i in range(width):
            for j in range(height):
                y[img.getpixel((i, j))] += 1
        plt.bar(x, y, color="grey")

    elif img.mode == 'RGB' or img.mode == 'RGBA':
        r = np.zeros(256, np.uint64)
        g = np.zeros(256, np.uint64)
        b = np.zeros(256, np.uint64)

        for i in range(width):
            for j in range(height):
                r[img.getpixel((i, j))[0]] += 1
                g[img.getpixel((i, j))[1]] += 1
                b[img.getpixel((i, j))[2]] += 1

        plt.bar(x, r, color="red", alpha=0.7, label="red")
        plt.bar(x, g, color="green", alpha=0.6, label="green")
        plt.bar(x, b, color="blue", alpha=0.5, label="blue")
        plt.legend(loc='upper right')

    plt.show(cmap="gray")


'''
Contract adjustment of a greyscale image by more equally spreading out the intensity values
of the image's histogram
'''


def histogram_equalize(kivy_img):
    img = Image.open(kivy_img.source)
    frequencies, r_frequencies, g_frequencies, b_frequencies = '', '', '', ''
    pixelMap = img.load()
    if img.mode == 'L':
        frequencies = np.zeros(256, np.uint64)
    elif img.mode == 'RGB' or img.mode == 'RGBA':
        r_frequencies = np.zeros(256, np.uint64)
        g_frequencies = np.zeros(256, np.uint64)
        b_frequencies = np.zeros(256, np.uint64)

    width, height = img.size

    if img.mode == 'L':
        for x in range(width):
            for y in range(height):
                frequencies[pixelMap[x, y]] += 1
        frequencies = np.divide(frequencies, (width * height))
    elif img.mode == 'RGB' or img.mode == 'RGBA':
        for x in range(width):
            for y in range(height):
                r_frequencies[pixelMap[x, y][0]] += 1
                g_frequencies[pixelMap[x, y][1]] += 1
                b_frequencies[pixelMap[x, y][2]] += 1
        r_frequencies = np.divide(r_frequencies, (width * height))
        g_frequencies = np.divide(g_frequencies, (width * height))
        b_frequencies = np.divide(b_frequencies, (width * height))

    if img.mode == 'L':
        cdf = 0
        for i, x in enumerate(frequencies):
            cdf += x
            frequencies[i] = round(255 * cdf)

        for x in range(width):
            for y in range(height):
                img.putpixel((x, y), int(frequencies[pixelMap[x, y]]))

    elif img.mode == 'RGB' or img.mode == 'RGBA':
        cdf_r = 0
        cdf_g = 0
        cdf_b = 0
        for i, (x1, x2, x3) in enumerate(zip(r_frequencies, g_frequencies, b_frequencies)):
            cdf_r += x1
            cdf_g += x2
            cdf_b += x3
            r_frequencies[i] = round(255 * cdf_r)
            g_frequencies[i] = round(255 * cdf_g)
            b_frequencies[i] = round(255 * cdf_b)

        for x in range(width):
            for y in range(height):
                pixelMap[x, y] = (int(r_frequencies[pixelMap[x, y][0]]), int(g_frequencies[pixelMap[x, y][1]]),
                                  int(b_frequencies[pixelMap[x, y][2]]))

    return img
