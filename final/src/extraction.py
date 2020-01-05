import numpy as np
import cv2

# cv2.namedWindow('image', cv2.WINDOW_NORMAL)

# #Load the Image
# imgo = cv2.imread('../img/help.jpg')
# height, width = imgo.shape[:2]

# #Create a mask holder
# mask = np.zeros(imgo.shape[:2],np.uint8)

# #Grab Cut the object
# bgdModel = np.zeros((1,65),np.float64)
# fgdModel = np.zeros((1,65),np.float64)

# #Hard Coding the Rect The object must lie within this rect.
# rect = (10,10,width-30,height-30)
# cv2.grabCut(imgo,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
# mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
# img1 = imgo*mask[:,:,np.newaxis]

# #Get the background
# background = imgo - img1

# #Change all pixels in the background that are not black to white
# background[np.where((background > [0,0,0]).all(axis = 2))] = [255,255,255]

# #Add the background and the image
# final = background + img1

# #To be done - Smoothening the edges

# cv2.imshow('image', final )
# cv2.imwrite('../img/girl_1.png', final)

# k = cv2.waitKey(0)

# if k==27:
#     cv2.destroyAllWindows()

def get_holes(image, thresh):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    im_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]
    im_bw_inv = cv2.bitwise_not(im_bw)

    contour, _ = cv2.findContours(im_bw_inv, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        cv2.drawContours(im_bw_inv, [cnt], 0, 255, -1)

    nt = cv2.bitwise_not(im_bw)
    im_bw_inv = cv2.bitwise_or(im_bw_inv, nt)
    return im_bw_inv


def remove_background(image, thresh, scale_factor=.25, kernel_range=range(1, 15), border=None):
    border = border or kernel_range[-1]

    holes = get_holes(image, thresh)
    small = cv2.resize(holes, None, fx=scale_factor, fy=scale_factor)
    bordered = cv2.copyMakeBorder(small, border, border, border, border, cv2.BORDER_CONSTANT)

    for i in kernel_range:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*i+1, 2*i+1))
        bordered = cv2.morphologyEx(bordered, cv2.MORPH_CLOSE, kernel)

    unbordered = bordered[border: -border, border: -border]
    mask = cv2.resize(unbordered, (image.shape[1], image.shape[0]))
    fg = cv2.bitwise_and(image, image, mask=mask)
    return fg


img = cv2.imread('../img/help.jpg')
nb_img = remove_background(img, 230)