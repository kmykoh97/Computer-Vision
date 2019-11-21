
import cv2
import numpy as np
from matplotlib import pyplot as plt
 
img = cv2.imread("../img/jaguar.jpg")
 
kernel = np.ones((5,5),np.uint8)
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
 
plt.subplot(121),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(gradient),plt.title('Dilation')
plt.xticks([]), plt.yticks([])
plt.show()