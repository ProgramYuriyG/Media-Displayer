import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib

'''
Visually display the greyscale intensity or color channel values of a given image
'''


# method to display the color/greyscale histogram of the image
def display_histogram(kivy_img):
    img = Image.open(kivy_img.source)
    plt.close()

    if img.mode == 'L':
        img_source = np.array(img.getdata())
        fig, ax = plt.subplots()
        n, bins, patches = ax.hist(img_source, bins=range(256), edgecolor='none')
        ax.set_title("Intensity Histogram")
        ax.set_xlim(0, 255)

        cm = plt.cm.get_cmap('cool')
        norm = matplotlib.colors.Normalize(vmin=bins.min(), vmax=bins.max())
        for b, p in zip(bins, patches):
            p.set_facecolor(cm(norm(b)))
        plt.xlabel("Color value")
        plt.ylabel("Pixels")
    elif img.mode == 'RGB' or img.mode == 'RGBA':
        img_source = np.array(img)
        colors = ("r", "g", "b")
        channel_ids = (0, 1, 2)

        plt.xlim([0, 256])
        for channel_id, c in zip(channel_ids, colors):
            histogram, bin_edges = np.histogram(
                img_source[:, :, channel_id], bins=256, range=(0, 256)
            )
            plt.plot(bin_edges[0:-1], histogram, color=c)

        plt.title("Intensity Histogram")
        plt.xlabel("Color value")
        plt.ylabel("Pixels")

    return plt


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
