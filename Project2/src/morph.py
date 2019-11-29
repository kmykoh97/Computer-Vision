import numpy as np
import cv2



KERNEL_SIZE = 3
KERNEL = 255*np.ones((KERNEL_SIZE,KERNEL_SIZE),np.uint8)

def add_padding(image,padding):
    return np.pad(image, (padding,padding), 'edge')

def erosion(image, kernel):
    h,w = image.shape[:2]
    res_img = np.zeros(image.shape,np.uint8)
    kl = len(kernel)
    k = len(kernel)//2
    padded_img = add_padding(image,k)
    for i in range(k, h+k):
        for j in range(k, w+k):
            submatrix = padded_img[i-k:i-k+kl,j-k:j-k+kl]
            ored = np.array_equal(submatrix,kernel)
            if ored == True:
                res_img[i-k][j-k] = 255
            else:
                res_img[i-k][j-k] = 0
    return res_img

def dilation(image, kernel):
    h,w = image.shape[:2]
    res_img = np.zeros(image.shape,np.uint8)
    kl = len(kernel)
    k = len(kernel)//2
    padded_img = add_padding(image,k)
    for i in range(k, h+k):
        for j in range(k, w+k):
            submatrix = padded_img[i-k:i-k+kl,j-k:j-k+kl]
            ored = np.logical_and(submatrix,kernel)
            if True in ored:
                res_img[i-k][j-k] = 255
            else:
                res_img[i-k][j-k] = 0
    return res_img   

def morphGradient(img, fname):
    print("morphological gradient")
    result = dilation(img.copy(),KERNEL) - erosion(img.copy(),KERNEL)
    cv2.imwrite(fname, result)

def morphEdgeDetection1(img, fname):
    print("morphological edge detection round 1")
    # Closing and then Opening
    img_d = dilation(img.copy(), KERNEL)
    img_d_e = erosion(img_d, KERNEL)
    img_d_e_e = erosion(img_d_e, KERNEL)
    img_d_e_e_d = dilation(img_d_e_e, KERNEL)
    img_erosion = erosion(img_d_e_e_d, KERNEL)
    result = img_d_e_e_d - img_erosion
    cv2.imwrite(fname, result)
    
def morphEdgeDetection2(img, fname):
    print("morphological edge detection round 2")
    # Opening then Closing
    img_e = erosion(img.copy(), KERNEL)
    img_e_d = dilation(img_e, KERNEL)
    img_e_d_d = dilation(img_e_d, KERNEL)
    img_e_d_d_e = erosion(img_e_d_d, KERNEL)
    img_erosion = erosion(img_e_d_d_e, KERNEL)
    result = img_e_d_d_e - img_erosion
    cv2.imwrite(fname, result)

def morphDilation(img, fname):
    print("morphological dilation")
    img_e = dilation(img.copy(), KERNEL)
    cv2.imwrite(fname, img_e)

def main():
    print("main")

if __name__ == '__main__':
    main()