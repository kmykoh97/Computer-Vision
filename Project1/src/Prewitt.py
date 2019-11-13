from PIL import Image
from sys import argv
import math



class Prewitt(object):
    def __init__(self, pathname):

        im = Image.open(pathname).convert('L')
        self.width, self.height = im.size
        mat = im.load()

        prewittx = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
        prewitty = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]

        self.prewittIm = Image.new('L', (self.width, self.height))
        pixels = self.prewittIm.load()

        # perform main iterations to process image pixels
        for row in range(self.width-len(prewittx)):
            for col in range(self.height-len(prewittx)):
                Gx = 0
                Gy = 0
                for i in range(len(prewittx)):
                    for j in range(len(prewitty)):
                        val = mat[row+i, col+j]
                        Gx += prewittx[i][j] * val
                        Gy += prewitty[i][j] * val

                pixels[row+1,col+1] = int(math.sqrt(Gx*Gx + Gy*Gy))

    def save(self, name):
        self.prewittIm.save(name)

def main(a, b):
    pathname = a
    inputname = pathname + '.' + b
    outputname = pathname + '_prewitt.' + b
    prewitt = Prewitt(inputname)
    prewitt.save(outputname)

# script, first, second = argv
# main(first, second)

# if __name__ == "__main__":
#     main("jaguar", "jpg")