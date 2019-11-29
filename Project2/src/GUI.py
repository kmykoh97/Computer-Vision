import os
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk
import ntpath
from morph import *
from reconstruction import *
import morph



# Placed outside function to access globally
root = tk.Tk()
root.geometry('600x200')
row1 = tk.Frame(root)
row2 = tk.Frame(root)
v = tk.IntVar()
kernelLabel = tk.Label(row1, text = "Kernel Size: ")
# sigmaLabel = tk.Label(row2, text = "Sigma: ")
kernelEntry = tk.Entry(row1, text=v)
v.set(3) # set default value of 3
# sigmaEntry = tk.Entry(row2)

def main():
    btn1 = tk.Button(root, text = 'Select Picture Here', bd = '5', command = inputPicture)
    btn2 = tk.Button(root, text = 'View Original Image', bd = '5', command = originalPictureView)
    btn3 = tk.Button(root, text = 'edge detection 1', bd = '5', command = edgeHelper1)
    btn4 = tk.Button(root, text = 'edge detection 2', bd = '5', command = edgeHelper2)
    btn5 = tk.Button(root, text = 'morph gradient', bd = '5', command = morphGradientHelper)
    btn6 = tk.Button(root, text = 'morph reconstruction', bd = '5', command = reconstructionHelper)
    btn7 = tk.Button(root, text = 'binary dilation', bd = '5', command = dilationHelper)
    # btn8 = tk.Button(root, text = 'Median', bd = '5', command = MedianHelper)
    btn9 = tk.Button(root, text = 'exit', bd = '5', command = root.destroy)
    padding = tk.Label(root, text="")
    btn1.pack(side='top')
    btn2.pack(side='top')
    padding.pack(side = tk.TOP)
    row1.pack(side = tk.TOP)
    kernelLabel.pack(side = tk.LEFT)
    kernelEntry.pack(side = tk.LEFT)
    row2.pack(side = tk.TOP)
    # sigmaLabel.pack(side = tk.LEFT)
    # sigmaEntry.pack(side = tk.LEFT)
    btn3.pack(side=tk.RIGHT)
    btn4.pack(side=tk.RIGHT)
    btn5.pack(side=tk.RIGHT)
    btn6.pack(side=tk.LEFT)
    btn7.pack(side=tk.LEFT)
    # btn8.pack(side=tk.LEFT)
    btn9.pack(side='bottom')
    root.title("main page")
    root.mainloop()
    print("Thank You!")

def inputPicture():
    global tmpimgpath # global variable fot other services
    tmpimgpath = filedialog.askopenfilename(initialdir=os.getcwd())

def originalPictureView():
    print("Original")
    root = tk.Toplevel()
    PictureLabel= tk.Label(root)
    PictureLabel.pack()
    selectedpicture = ImageTk.PhotoImage(file=tmpimgpath)
    PictureLabel.configure(image=selectedpicture)
    root.title("Original Image")
    root.mainloop()

def edgeHelper1():
    # print("Morphological Edge Detection")
    morph.KERNEL_SIZE = int(kernelEntry.get())
    pathname = ntpath.dirname(tmpimgpath)
    outputname = pathname + "/medge1.jpg"
    img = cv2.imread(tmpimgpath, 0)
    morphEdgeDetection1(img, outputname)
    root = tk.Toplevel()
    PictureLabel= tk.Label(root)
    PictureLabel.pack()
    selectedpicture = ImageTk.PhotoImage(file=outputname)
    PictureLabel.configure(image=selectedpicture)
    root.title("morphological edge detection 1 Result")
    root.mainloop()

def edgeHelper2():
    # print("Morphological Edge Detection")
    morph.KERNEL_SIZE = int(kernelEntry.get())
    pathname = ntpath.dirname(tmpimgpath)
    outputname = pathname + "/medge2.jpg"
    img = cv2.imread(tmpimgpath, 0)
    morphEdgeDetection2(img, outputname)
    root = tk.Toplevel()
    PictureLabel= tk.Label(root)
    PictureLabel.pack()
    selectedpicture = ImageTk.PhotoImage(file=outputname)
    PictureLabel.configure(image=selectedpicture)
    root.title("morphological edge detection 2 Result")
    root.mainloop()

def dilationHelper():
    # print("Morphological Edge Detection")
    morph.KERNEL_SIZE = int(kernelEntry.get())
    pathname = ntpath.dirname(tmpimgpath)
    outputname = pathname + "/dilation.jpg"
    img = cv2.imread(tmpimgpath, 0)
    morphEdgeDetection1(img, outputname)
    root = tk.Toplevel()
    PictureLabel= tk.Label(root)
    PictureLabel.pack()
    selectedpicture = ImageTk.PhotoImage(file=outputname)
    PictureLabel.configure(image=selectedpicture)
    root.title("morphological binary dilation Result")
    root.mainloop()

def morphGradientHelper():
    # print("Morphological Gradient")
    morph.KERNEL_SIZE = int(kernelEntry.get())
    pathname = ntpath.dirname(tmpimgpath)
    outputname = pathname + "/mgradient.jpg"
    img = cv2.imread(tmpimgpath, 0)
    morphGradient(img, outputname)
    root = tk.Toplevel()
    PictureLabel= tk.Label(root)
    PictureLabel.pack()
    selectedpicture = ImageTk.PhotoImage(file=outputname)
    PictureLabel.configure(image=selectedpicture)
    root.title("morphological Gradient Result")
    root.mainloop()

def reconstructionHelper():
    print("Morphological Reconstruction")
    pathname = ntpath.dirname(tmpimgpath)
    outputname = pathname + "/mreconstruction.jpg"
    img = cv2.imread(tmpimgpath)
    recon(img)
    root = tk.Toplevel()
    PictureLabel= tk.Label(root)
    PictureLabel.pack()
    # selectedpicture = ImageTk.PhotoImage(file=outputname)
    # PictureLabel.configure(image=selectedpicture)
    root.title("morphological Reconstruction Result")
    root.mainloop()

if __name__ == "__main__":
    main()