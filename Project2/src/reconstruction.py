# import libraries
import cv2
from matplotlib import pyplot as plt
import numpy as np

# choose between 3 images
def get_image():
    while True:
        try:
            choice = int(input("\nEnter 1(binary) or 2(grayscale) or 3(color) for img: "))
            if (choice == 1):
                im = 'bimg.png'
            elif (choice == 2):
                im = 'gimg.png'
            elif (choice == 3):
                im = '../img/jaguar.jpg'

        except ValueError:
            print("\n1, 2, or 3.\n")
        else:
            # check if constant is in range
            if choice in range(1,4):
                break
            else:
                print("\n1, 2, or 3.\n")
    return (im)

# open an image
choice = get_image()

# reads image as grayscale (only 1 channel)
image = cv2.imread(choice, 0)

# Check if image is binary
# https://stackoverflow.com/questions/40595967/fast-way-to-check-if-a-numpy-array-is-binary-contains-only-0-and-1
def is_binary(img):
    # if any pixel value is not 0 or 255, return False
    return ((img == 0) | (img == 255)).all()

# Convert image if not binary
def convert_img2b(img):
    # threshold/segment image to 0 or 255
    ret, bimg = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    return bimg.astype(np.uint8)

# check and convert image to binary if necessary
if (is_binary(image)):
    # if binary
    # copy image into img
    img = image.copy()
else:
    # convert image to binary if not
    img = convert_img2b(image)

# form marker image f
# input should be inverted image
def marker_f(img):
    # get size of original image
    x, y = img.shape

    # create empty array to hold values for marker image
    f = np.zeros((x,y))
    #https: // stackoverflow.com / questions / 47772299 / how - to - get - border - pixels - of - an - image - in -python
    # width of border (1px)
    bw = 1
    # keep only border of original image
    # create mask for the border of image
    # 255 border, 0 inside border
    mask1 = 255 * np.ones(img.shape[:2], dtype="uint8")
    mask1 = cv2.rectangle(mask1, (bw, bw), (img.shape[1] - bw - 1, img.shape[0] - bw - 1), 0, -1)

    # apply mask to image (inverted image is input to function)
    # anything inside the border becomes 0
    # anything on the border stays the same
    f = cv2.bitwise_and(img, mask1)

    return f

# 0 = black
# 255 = white

# form mask g
# input should be original image
def mask_g(img):
    # get size of original image
    x, y = img.shape

    # create empty array to hold values for marker image
    g = np.zeros((x,y))

    # invert values
    g = ~img

    return g

# get mask g
# inverted image
g = mask_g(img)

# get marker image f
f = marker_f(g)

# morphological reconstruction via dilation
def morphrecon(f, g):
    # create 3x3 structuring element
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # https: // www.quora.com / How - do - I - reconstruct - an - image - morphologically - using - the - erosion - function - in -Matlab
    # set first recon as marker image
    # f = inverted border of original image
    recon = f

    # empty array for reconstruction
    # get size of image
    x, y = f.shape

    # create empty array to hold values for marker image
    recon_old = np.zeros((x, y), dtype= np.uint8)

    # count iterations needed
    iterations = 0

    # repeat until n = n-1
    while not np.array_equal(recon, recon_old):
        iterations = iterations + 1
        recon_old = recon.copy()

        # min returns the lowest value
        # 0 if either recon_old or g has a 0, 255 only when both are 255
        # functions as an intersect operation
        # bitwise_and also works
        recon = cv2.min(cv2.dilate(recon_old, se), g)

    # invert final reconstruction
    return ~recon, ~recon_old, iterations

recon, recon_old, iterations = morphrecon(f, g)


# display via cv2
cv2.imshow('original image', image)
cv2.imshow('thresholded image (if greyscale or color)', img)
cv2.imshow('marker image f', f)
cv2.imshow('mask g (inverted image)', g)
cv2.imshow('previous reconstructed image', recon_old)
cv2.imshow('reconstructed image ,i = %d' %iterations, recon)


# display via matplotlib
# display images
fig = plt.figure(0)
fig.canvas.set_window_title('Filling in white objects via Morphological Reconstruction')

plt.subplot(3, 2, 1)
plt.title("Original Image")
plt.axis('off')
plt.imshow(image, cmap = 'gray')

plt.subplot(3, 2, 2)
plt.title("Binary Image")
plt.axis('off')
plt.imshow(img, cmap= 'gray')

plt.subplot(3, 2, 3)
plt.title("Marker Image F")
plt.axis('off')
plt.imshow(f, cmap= 'gray')

plt.subplot(3, 2, 4)
plt.title("Mask G, inverted image")
plt.axis('off')
plt.imshow(g, cmap= 'gray')

plt.subplot(3, 2, 5)
plt.title("Previous Reconstructed Image")
plt.axis('off')
plt.imshow(recon_old, cmap= 'gray')

plt.subplot(3, 2, 6)
plt.title("Reconstructed Image, Iterations = %d" % iterations)
plt.axis('off')
plt.imshow(recon, cmap= 'gray')

plt.show()

cv2.waitKey(0)