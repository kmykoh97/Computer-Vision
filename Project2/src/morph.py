import numpy as np
import cv2

KERNEL_SIZE = 3
KERNEL = 255*np.ones((KERNEL_SIZE,KERNEL_SIZE),np.uint8)

#Read the image using opencv
def get_image(path):
    return cv2.imread(path)

#Read the image in gray scale using opencv
def get_image_gray(path):
    return cv2.imread(path,0)

#Show the resulting image
def show_image(name, image):
    cv2.imshow(name,image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#Save the resulting image
def save_image(name, image):
    cv2.imwrite(name,image) 

#Add Zero padding around the edge of the image
def add_padding(image,padding):
    return np.pad(image, (padding,padding), 'edge')

#Perform normalization on the image
def norm(image):
    return (image/255).astype(np.uint8)

#Copy the image
def copy(image):
    return image.copy()

#Perform erosion on the given image
def erosion(image, kernel):
    h,w = image.shape[:2]
    res_img = np.zeros(image.shape,np.uint8)
    kl = len(kernel)
    k = len(kernel)//2
    padded_img = add_padding(image,k)
    for i in range(k, h+k):
        for j in range(k, w+k):
            submatrix = padded_img[i-k:i-k+kl,j-k:j-k+kl]
            #If both the kernel and the underlying pixels of the image (submatrix)
            #are equal, then set to 255 (1) else set to 0
            ored = np.array_equal(submatrix,kernel)
            if ored == True:
                res_img[i-k][j-k] = 255
            else:
                res_img[i-k][j-k] = 0
    return res_img

#Perform dilation on the given image
def dilation(image, kernel):
    h,w = image.shape[:2]
    res_img = np.zeros(image.shape,np.uint8)
    kl = len(kernel)
    k = len(kernel)//2
    padded_img = add_padding(image,k)
    for i in range(k, h+k):
        for j in range(k, w+k):
            submatrix = padded_img[i-k:i-k+kl,j-k:j-k+kl]
            #If there is any one match between the kernel and the underlying pixels
            #then set to 255 (1) else set to 0
            ored = np.logical_and(submatrix,kernel)
            if True in ored:
                res_img[i-k][j-k] = 255
            else:
                res_img[i-k][j-k] = 0
    return res_img   

#Extract the boundary by subtracting given image
#With the erosion of the given image
def extract_boundary(oimg, eimg):
    return oimg - eimg

def main():
    print("__Reading the given image : ../original_imgs/noise.jpg__")
    img = get_image_gray('../img/1.jpg')
    
    # print('\n__Performing Opening and then Closing__')
    # #Opening and then Closing
    # img_e = erosion(img.copy(),KERNEL)
    # img_e_d = dilation(img_e,KERNEL)
    # img_e_d_d = dilation(img_e_d,KERNEL)
    # img_e_d_d_e = erosion(img_e_d_d,KERNEL)
    # save_image('res_noise1.jpg', img_e_d_d_e)

    # print('\n__Performing Closing and then Opening__')
    # #Closing and then Opening
    # img_d = dilation(img,KERNEL)
    # img_d_e = erosion(img_d,KERNEL)
    # img_d_e_e = erosion(img_d_e,KERNEL)
    # img_d_e_e_d = dilation(img_d_e_e,KERNEL)
    # save_image('res_noise2.jpg', img_d_e_e_d)    

    # print('\n__Performing Boundary Extraction on res_noise1.jpg__')
    # #Boundary 1
    # img_erosion = erosion(img_e_d_d_e,KERNEL)
    # boundary_1 = extract_boundary(img_e_d_d_e,img_erosion)
    # save_image('res_bound1.jpg', boundary_1)

    # print('\n__Performing Boundary Extraction on res_noise2.jpg__')
    # #Boundary 2
    # img_dilation = erosion(img_d_e_e_d,KERNEL)
    # boundary_2 = extract_boundary(img_d_e_e_d,img_dilation)
    # save_image('res_bound2.jpg', boundary_2)

    imae = cv2.imread("../img/jaguar.jpg")
    gradient = cv2.morphologyEx(imae, cv2.MORPH_GRADIENT, KERNEL)
    cv2.imwrite("../img/ex.jpg", gradient)

if __name__ == '__main__':
    main()