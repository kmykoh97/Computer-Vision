import cv2
import numpy as np


def erosion(img, kernel):
    new_img = [[0]*351 for i in range(img.shape[0])]
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            new_img[i][j] = kernel[0][0]*img[i-1][j-1] and kernel[0][1]*img[i-1][j] and kernel[0][2]*img[i-1][j+1] \
                                and kernel[1][0] * img[i][j - 1] and kernel[1][1]*img[i][j] and \
                                kernel[1][2]*img[i][j+1] and kernel[2][0] * img[i+1][j - 1] and \
                                kernel[2][1]*img[i+1][j] and kernel[2][2]*img[i+1][j+1]

    new_img = np.asarray(new_img)
    return new_img


def dilation(img, kernel):
    new_img = [[0] * 351 for i in range(img.shape[0])]
    for i in range(1, img.shape[0] - 1):
        for j in range(1, img.shape[1] - 1):
            new_img[i][j] = kernel[0][0] * img[i - 1][j - 1] or kernel[0][1] * img[i - 1][j] or kernel[0][2] * \
                                  img[i - 1][j + 1] or kernel[1][0] * img[i][j - 1] or kernel[1][1] * img[i][j] or \
                                  kernel[1][2] * img[i][j + 1] or kernel[2][0] * img[i + 1][j - 1] or kernel[2][1] * \
                                  img[i + 1][j] or kernel[2][2] * img[i + 1][j + 1]

    new_img = np.asarray(new_img)
    return new_img


def opening(img, kernel):
    image_1 = erosion(img, kernel)
    image_2 = dilation(image_1, kernel)
    return image_2


def closing(img, kernel):
    image_1 = dilation(img, kernel)
    image_2 = erosion(image_1, kernel)
    return image_2


def algorithm_1(img, kernel):
    image_1 = opening(img, kernel)
    image_2 = closing(image_1, kernel)
    return image_2


def algorithm_2(img, kernel):
    image_1 = closing(img, kernel)
    image_2 = opening(image_1, kernel)
    return image_2


def boundary_extraction(img, kernel):
    image_1 = dilation(img, kernel)
    return image_1 - img


image = cv2.imread("input_images/noise.jpg", 0)

k = np.ones((3, 3), np.uint8)

print("shape:", image.shape)

img_1 = algorithm_1(image, k)
cv2.imwrite("res_noise1.jpg", img_1)

img_2 = algorithm_2(image, k)
cv2.imwrite("res_noise2.jpg", img_2)

img_3 = boundary_extraction(img_1, k)
cv2.imwrite("res_bound1.jpg", img_3)

img_4 = boundary_extraction(img_2, k)
cv2.imwrite("res_bound2.jpg", img_4)