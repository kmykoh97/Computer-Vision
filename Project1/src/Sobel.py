from PIL import Image
from sys import argv
import math



class Sobel(object):
    def __init__(self, pathname):

        self.im = Image.open(pathname).convert('L') # convert to greyscale
        self.width, self.height = self.im.size
        mat = self.im.load()

        # Sobel convolution kernels
        sobelx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        sobely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

        self.sobelIm = Image.new('L', (self.width, self.height))
        pixels = self.sobelIm.load()

        #For each pixel in the image
        for row in range(self.width-len(sobelx)):
            for col in range(self.height-len(sobelx)):
                Gx = 0
                Gy = 0
                for i in range(len(sobelx)):
                    for j in range(len(sobely)):
                        val = mat[row+i, col+j]
                        Gx += sobelx[i][j] * val
                        Gy += sobely[i][j] * val

                pixels[row+1,col+1] = int(math.sqrt(Gx*Gx + Gy*Gy))

    def save(self, name):
        self.sobelIm.save(name)


def main(a, b):
    pathname = '../img/' + a
    inputname = pathname + '.' + b
    outputname = pathname + '_sobel.' + b
    sobel = Sobel(inputname)
    sobel.save(outputname)

# script, first, second = argv
# main(first, second)

# if __name__ == "__main__":
#     main("jaguar", "jpg")

