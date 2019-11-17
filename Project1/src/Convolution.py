import numpy as np
from PIL import Image
import os
import math



class Convolution:
    def __init__(self, pathname, kernel, sigma):
        self.kernel_size = kernel
        self.sigma_size = sigma
        self.image = self.load_image(pathname)
        self.result = np.ndarray(self.image.size)

    def load_image(self, pathname):
        im = Image.open(pathname).convert('L')
        return np.array(im)

    def save(self, pathname):
        im = Image.fromarray(self.result).convert('RGB')
        im.save(pathname)

    def apply_median_filter(self):
        image = self.image
        size = self.kernel_size
        pad = int((size - 1) / 2)
        width = image.shape[0] - (2 * pad)
        height = image.shape[1] - (2 * pad)
        filtered_image = np.ndarray((width, height))
        for i in range(pad, image.shape[0] - pad):
            for j in range(pad, image.shape[1] - pad):
                filtered_image[i-pad, j-pad] = np.sort(image[i - pad:i + pad + 1, j - pad:j + pad + 1].flatten())[int(((size*size)-1)/2)]
        self.result = filtered_image
        return filtered_image

    def generate_gaussian_kernel(self, dim, sigma):
        kernel = np.ndarray((dim, dim))
        center = int((dim-1)/2)
        coeff = 1/((sigma**2)*2*math.pi)
        exp_denum = 2*(sigma**2)
        for i in range(kernel.shape[0]):
            exp_x = (i-center)**2
            for j in range(kernel.shape[1]):
                exp_y = (j-center)**2
                kernel[i, j] = coeff * math.exp(-1*(exp_x + exp_y)/exp_denum)
        return kernel

    def apply_gaussian_filter(self):
        sigma = self.sigma_size
        kernel_size = self.kernel_size
        kernel = self.generate_gaussian_kernel(kernel_size, sigma)
        filtered_image = self.apply_filter(kernel)
        self.result = filtered_image
        return filtered_image

    def generate_mean_kernel(self, dim):
        value = 1/(dim**2)
        kernel = np.full((dim, dim), value)
        return kernel

    def apply_mean_filter(self):
        kernel_size = self.kernel_size
        kernel = self.generate_mean_kernel(kernel_size)
        filtered_image = self.apply_filter(kernel)
        self.result = filtered_image
        return filtered_image

    def apply_filter(self, kernel):
        image = self.image
        pad = int((kernel.shape[0]-1)/2)
        width = image.shape[0]-(2*pad)
        height = image.shape[1]-(2*pad)
        filtered_image = np.ndarray((width, height))
        for i in range(pad, image.shape[0]-pad):
            for j in range(pad, image.shape[1]-pad):
                filtered_image[i-pad, j-pad] = np.sum(image[i-pad:i+pad+1, j-pad:j+pad+1]*kernel)
        self.result = filtered_image
        return filtered_image

# def main():
#     print("Hello World, Convolution!!!")

# if __name__ == "__main__":
#     main()
