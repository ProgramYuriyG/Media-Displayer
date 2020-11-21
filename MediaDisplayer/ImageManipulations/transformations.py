import numpy as np
from PIL import Image
import cv2


def colortogrey(kivy_img):
    return Image.open(kivy_img.source).convert('L')


'''
Negative Transformation: each intensity value of the input image is subtracted from L-1, inversing the value
'''


def negativetransform(kivy_img):
    img = Image.open(kivy_img.source)
    row, col = img.size
    pixelMap = img.load()
    if img.mode == 'L':
        for i in range(0, row):
            for j in range(0, col):
                pixelMap[i, j] = 255 - pixelMap[i, j]
    elif img.mode == 'RGB' or img.mode == 'RGBA':
        for i in range(0, row):
            for j in range(0, col):
                r = 255 - pixelMap[i, j][0]
                g = 255 - pixelMap[i, j][1]
                b = 255 - pixelMap[i, j][2]
                pixelMap[i, j] = (r, g, b)
    return img


"""
Binary Transformation: Setting of pixel intensity values based on whether or not original value is within threshold:
    if intensityVal < t, intensityVal = 0
       intensityVal >= t, intensityVal = 255
"""


def binarytransform(kivy_img, t):
    img = Image.open(kivy_img.source)
    row, col = img.size
    pixelMap = img.load()

    if img.mode == 'L':
        for i in range(0, row):
            for j in range(0, col):
                if pixelMap[i, j] < t:
                    pixelMap[i, j] = 0
                else:
                    pixelMap[i, j] = 255
    elif img.mode == 'RGB' or img.mode == 'RGBA':
        for i in range(0, row):
            for j in range(0, col):
                r = pixelMap[i, j][0]
                g = pixelMap[i, j][1]
                b = pixelMap[i, j][2]
                if r < t:
                    r = 0
                else:
                    r = 255
                if g < t:
                    g = 0
                else:
                    g = 255
                if b < t:
                    b = 0
                else:
                    b = 255
                pixelMap[i, j] = (r, g, b)
    return img


"""
Multilevel Transformation: Intensity value bound by two threshold values t1, t2 that determine the adjusted value:
    if intensityVal < t1 or intensityVal > t2, intensityVal = 0
       t1 <= intensityVal <= t2, intensityVal is unchanged
"""


def multileveltransform(kivy_img, t1, t2):
    img = Image.open(kivy_img.source)
    row, col = img.size
    pixelMap = img.load()

    if img.mode == 'L':
        for i in range(0, row):
            for j in range(0, col):
                if pixelMap[i, j] < t1 or pixelMap[i, j] > t2:
                    pixelMap[i, j] = 0
    elif img.mode == 'RGB' or img.mode == 'RGBA':
        for i in range(0, row):
            for j in range(0, col):
                r = pixelMap[i, j][0]
                g = pixelMap[i, j][1]
                b = pixelMap[i, j][2]
                if r < t1 or r > t2:
                    r = 0
                if g < t1 or g > t2:
                    g = 0
                if b < t1 or b > t2:
                    b = 0
                pixelMap[i, j] = (r, g, b)
    return img


'''
Logarithmic transformation of input image.
Dark pixels are expanded and higher pixel values are compressed, resulting in a lighter image
'''


def logtransform(kivy_img):
    img = Image.open(kivy_img.source)
    c = 255 / np.log10(1 + np.max(img))
    row, col = img.size
    pixelMap = img.load()

    if img.mode == 'L':
        for i in range(0, row):
            for j in range(0, col):
                pixelMap[i, j] = round(c * np.log10(1 + abs(pixelMap[i, j])))
    elif img.mode == 'RGB' or img.mode == 'RGBA':
        for i in range(0, row):
            for j in range(0, col):
                r = pixelMap[i, j][0]
                g = pixelMap[i, j][1]
                b = pixelMap[i, j][2]
                r = round(c * np.log10(1 + abs(r)))
                g = round(c * np.log10(1 + abs(g)))
                b = round(c * np.log10(1 + abs(b)))
                pixelMap[i, j] = (r, g, b)
    return img


'''
Gamma transformation of input image.
If gamma < 1, dark values expanded, bright values compressed (lighter image)
If gamma > 1, dark values compressed, bright values expanded (darker image)
'''


def gammatransform(kivy_img, gamma):
    img = Image.open(kivy_img.source)
    c = 255 / (255 ** gamma)
    row, col = img.size
    pixelMap = img.load()

    if img.mode == 'L':
        for i in range(0, row):
            for j in range(0, col):
                pixelMap[i, j] = round(c * (pixelMap[i, j] ** gamma))
    elif img.mode == 'RGB' or img.mode == 'RGBA':
        for i in range(0, row):
            for j in range(0, col):
                r = pixelMap[i, j][0]
                g = pixelMap[i, j][1]
                b = pixelMap[i, j][2]
                r = round(c * (r ** gamma))
                g = round(c * (g ** gamma))
                b = round(c * (b ** gamma))
                pixelMap[i, j] = (r, g, b)
    return img


"""
Adaptive Integrated Neighborhood Dependent Approach for Nonlinear Enhancement
Method for enhancing the color of images
"""


def aindane(kivy_img, lmda):
    img = Image.open(kivy_img.source)
    original_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    b, g, r = (cv2.split(np.float64(original_img)))

    # conversion of original image to greyscale
    img_grey = (((76.245 * r) + (149.685 * g) + (29.070 * b)) / 255).astype('uint8')

    # normalization of greyscale image
    img_norm = img_grey / 255.0

    # determination of intensity value at 10% of cdf
    hist = cv2.calcHist([img_grey], [0], None, [256], [0, 256])
    cdf = hist.cumsum() / np.sum(hist)
    L = np.where(cdf >= 0.1)[0][0]

    if L <= 50:
        z = 0
    elif 50 < L <= 150:
        z = (L - 50) / 100
    else:
        z = 1

    # application of luminance enhancement nonlinear transfer function
    img_norm_prime = (img_norm ** (0.75 * z + 0.25) + (1 - img_norm) * 0.4 * (1 - z) + (img_norm ** (2 - z))) / 2

    stdev = int(np.std(img_grey))

    # acquisition of the Gaussian kernel convolved image
    kernel = cv2.getGaussianKernel(stdev*2, stdev)
    img_conv = cv2.sepFilter2D(img_grey, -1, kernel, kernel)

    if stdev <= 3:
        p = 3
    elif 3 < stdev < 10:
        p = (27 - 2 * stdev) / 7
    else:
        p = 1

    # application of center-surround contrast enhancement
    # addition of 1e-6 is to prevent division by 0 errors
    img_e = (img_conv / (img_grey + 1e-6)) ** p

    img_s = 255 * (img_norm_prime ** img_e)

    # application of color restoration step

    # addition of 1e-6 is to prevent division by 0 errors
    b = (img_s * (b / (img_grey + 1e-6)) * lmda).astype(np.uint8)
    g = (img_s * (g / (img_grey + 1e-6)) * lmda).astype(np.uint8)
    r = (img_s * (r / (img_grey + 1e-6)) * lmda).astype(np.uint8)

    # merging of color channels to get our enhanced color image
    img_enhanced = cv2.merge((r, g, b))

    img_enhanced = Image.fromarray(img_enhanced)
    return img_enhanced
