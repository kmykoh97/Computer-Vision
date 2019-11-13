import os
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk
import ntpath
from Prewitt import Prewitt
from Roberts import Roberts
from Sobel import Sobel
from Convolution import Convolution



# Placed outside function to access globally
root = tk.Tk()
root.geometry('350x250')
row1 = tk.Frame(root)
row2 = tk.Frame(root)
kernelLabel = tk.Label(row1, text = "Kernel Size: ")
sigmaLabel = tk.Label(row2, text = "Sigma: ")
kernelEntry = Entry(row1)
sigmaEntry = Entry(row2)

def main():
    btn1 = tk.Button(root, text = 'Select Picture Here', bd = '5', command = inputPicture)
    btn2 = tk.Button(root, text = 'View Original Image', bd = '5', command = originalPictureView)
    btn3 = tk.Button(root, text = 'Prewitt', bd = '5', command = PrewittHelper)
    btn4 = tk.Button(root, text = 'Roberts', bd = '5', command = RobertsHelper)
    btn5 = tk.Button(root, text = 'Sobel', bd = '5', command = SobelHelper)
    btn6 = tk.Button(root, text = 'Gaussian', bd = '5', command = GaussionHelper)
    btn7 = tk.Button(root, text = 'Mean', bd = '5', command = MeanHelper)
    btn8 = tk.Button(root, text = 'Median', bd = '5', command = MedianHelper)
    btn9 = tk.Button(root, text = 'exit', bd = '5', command = root.destroy)
    padding = tk.Label(root, text="")
    btn1.pack(side='top')
    btn2.pack(side='top')
    padding.pack(side = tk.TOP)
    row1.pack(side = tk.TOP)
    kernelLabel.pack(side = tk.LEFT)
    kernelEntry.pack(side = tk.LEFT)
    row2.pack(side = tk.TOP)
    sigmaLabel.pack(side = tk.LEFT)
    sigmaEntry.pack(side = tk.LEFT)
    btn3.pack(side=tk.RIGHT)
    btn4.pack(side=tk.RIGHT)
    btn5.pack(side=tk.RIGHT)
    btn6.pack(side=tk.LEFT)
    btn7.pack(side=tk.LEFT)
    btn8.pack(side=tk.LEFT)
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

def PrewittHelper():
    print("Prewitt")
    pathname = ntpath.dirname(tmpimgpath)
    outputname = pathname + "/prewittoutput.jpg"
    prewitt = Prewitt(tmpimgpath)
    prewitt.save(outputname)
    root = tk.Toplevel()
    PictureLabel= tk.Label(root)
    PictureLabel.pack()
    selectedpicture = ImageTk.PhotoImage(file=outputname)
    PictureLabel.configure(image=selectedpicture)
    root.title("Prewitt Result")
    root.mainloop()

def RobertsHelper():
    print("Roberts")
    pathname = ntpath.dirname(tmpimgpath)
    outputname = pathname + "/robertsoutput.jpg"
    roberts = Roberts(tmpimgpath)
    roberts.save(outputname)
    root = tk.Toplevel()
    PictureLabel= tk.Label(root)
    PictureLabel.pack()
    selectedpicture = ImageTk.PhotoImage(file=outputname)
    PictureLabel.configure(image=selectedpicture)
    root.title("Roberts Result")
    root.mainloop()

def SobelHelper():
    print("Sobel")
    pathname = ntpath.dirname(tmpimgpath)
    outputname = pathname + "/sobeloutput.jpg"
    sobel = Sobel(tmpimgpath)
    sobel.save(outputname)
    root = tk.Toplevel()
    PictureLabel= tk.Label(root)
    PictureLabel.pack()
    selectedpicture = ImageTk.PhotoImage(file=outputname)
    PictureLabel.configure(image=selectedpicture)
    root.title("Sobel Result")
    root.mainloop()

def GaussionHelper():
    print("Gaussion Filter")
    pathname = ntpath.dirname(tmpimgpath)
    outputname = pathname + "/gaussionoutput.jpg"
    gaussian = Convolution(tmpimgpath, int(kernelEntry.get()), int(sigmaEntry.get()))
    gaussian.apply_gaussian_filter()
    gaussian.save(outputname)
    root = tk.Toplevel()
    PictureLabel= tk.Label(root)
    PictureLabel.pack()
    selectedpicture = ImageTk.PhotoImage(file=outputname)
    PictureLabel.configure(image=selectedpicture)
    root.title("Gaussion Filter Result")
    root.mainloop()
    
def MeanHelper():
    print("Mean Filter")
    pathname = ntpath.dirname(tmpimgpath)
    outputname = pathname + "/meanoutput.jpg"
    mean = Convolution(tmpimgpath, int(kernelEntry.get()), int(sigmaEntry.get()))
    mean.apply_mean_filter()
    mean.save(outputname)
    root = tk.Toplevel()
    PictureLabel= tk.Label(root)
    PictureLabel.pack()
    selectedpicture = ImageTk.PhotoImage(file=outputname)
    PictureLabel.configure(image=selectedpicture)
    root.title("Mean Filter Result")
    root.mainloop()

def MedianHelper():
    print("Median Fiter")
    pathname = ntpath.dirname(tmpimgpath)
    outputname = pathname + "/medianoutput.jpg"
    median = Convolution(tmpimgpath, int(kernelEntry.get()), int(sigmaEntry.get()))
    median.apply_median_filter()
    median.save(outputname)
    root = tk.Toplevel()
    PictureLabel= tk.Label(root)
    PictureLabel.pack()
    selectedpicture = ImageTk.PhotoImage(file=outputname)
    PictureLabel.configure(image=selectedpicture)
    root.title("Median Filter Result")
    root.mainloop()

if __name__ == "__main__":
    main()