from PIL import Image
from sys import argv
import math



class Roberts(object):
    def __init__(self, pathname):
        im = Image.open(pathname).convert('L')
        self.width, self.height = im.size
        mat = im.load()

        # Roberts Cross convolution kernels
        robertsx = [[1,0],[0,-1]]
        robertsy = [[0,1],[-1,0]]
        self.sobelIm = Image.new('L', (self.width, self.height))
        pixels = self.sobelIm.load()

        # for each pixel in the image
        for row in range(self.width-len(robertsx)):
            for col in range(self.height-len(robertsy)):
                Gx = 0
                Gy = 0

                # iterate pixels in each kernels block
                for i in range(len(robertsx)):
                    for j in range(len(robertsy)):
                        val = mat[row+i, col+j]
                        Gx += robertsx[i][j] * val
                        Gy += robertsy[i][j] * val
                pixels[row+1,col+1] = int(math.sqrt(Gx*Gx + Gy*Gy))

    def save(self, name):
        self.sobelIm.save(name)

# def main(a, b):
#     pathname = '../img/' + a
#     inputname = pathname + '.' + b
#     outputname = pathname + '_roberts.' + b
#     roberts = Roberts(inputname)
#     roberts.save(outputname)

# script, first, second = argv
# main(first, second)

# if __name__ == "__main__":
#     main("jaguar", "jpg")