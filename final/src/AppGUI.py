import tkinter as tk
import tkinter.filedialog as fd
from tkinter import ttk
from tkinter.simpledialog import askinteger, askfloat, askstring
import BottleCapDealer as BCD
import tkinter.messagebox as tm
from PIL import Image, ImageTk
import numpy as np


class AppGUI:
    # img_dealer = ID.ImageDealing()
    img_dealer = BCD.BottleCapDealer()
    my_res = 0
    img_loaded = False
    img_res = 0
    data_res = 0

    def __init__(self, width, height, title):
        self.mainWindow = tk.Tk()
        self.mainWindow.title = title
        self.mainWindow.geometry(str(width) + "x" + str(height))

        self.init_canvas = self.create_canvas()
        self.init_canvas.place(x=25, y=50, anchor="nw")
        tk.Label(self.mainWindow, text="原始图片").place(x=325, y=25, anchor="n")

        self.my_res_canvas = self.create_canvas()
        self.my_res_canvas.place(x=650, y=50, anchor="nw")
        tk.Label(self.mainWindow, text="标记后的图片").place(x=950, y=25, anchor="n")

        self.menu_bar = tk.Menu(self.mainWindow)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)
        self.file_menu.add_command(label="导入图片", command=self.load_img)
        self.file_menu.add_command(label="标记瓶盖", command=self.img_op(self.find_caps_op))

        self.data_columns = ("序号", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.pos_data = ttk.Treeview(self.mainWindow, show="headings", columns=self.data_columns, height=3)

        for col in self.data_columns:
            self.pos_data.column(col, width=60, anchor="center")
            self.pos_data.heading(col, text=col)

        self.pos_data.place(x=637, y=550, anchor="n")
        tk.Label(self.mainWindow, text="标记数据").place(x=637, y=525, anchor="n")

        self.mainWindow.config(menu=self.menu_bar)

    def create_canvas(self):
        new_canvas = tk.Canvas(self.mainWindow, width=600, height=450, bg="white", scrollregion=(0, 0, 600, 450))
        y_scroll = tk.Scrollbar(new_canvas, orient=tk.VERTICAL)
        x_scroll = tk.Scrollbar(new_canvas, orient=tk.HORIZONTAL)
        new_canvas.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
        y_scroll.configure(command=new_canvas.yview)
        x_scroll.configure(command=new_canvas.xview)
        y_scroll.place(x=600, width=20, height=450)
        x_scroll.place(y=450, width=600, height=20)
        return new_canvas

    def run(self):
        self.mainWindow.mainloop()

    def load_img(self):
        self.img_loaded = True
        img_name = fd.askopenfilename()
        self.img_dealer.read_img(img_name)
        img_show = ImageTk.PhotoImage(self.img_dealer.img_pil.resize((600, 450), Image.ANTIALIAS))
        self.show_img(self.init_canvas, img_show)

    @staticmethod
    def show_img(canvas, img):
        canvas.create_image(0, 0, anchor="nw", image=img)
        canvas.config(scrollregion=(0, 0, img.width(), img.height()))
        canvas.image = img

    @staticmethod
    def no_img_error():
        tm.showerror(title="未导入图片", message="未导入图片，无法标记，请先导入图片")

    def find_caps_op(self):
        img_res, data_res = self.img_dealer.dealing_process()
        self.display_my_result(img_res)
        x_data = ["坐标x"]
        y_data = ["坐标y"]
        state_data = ["姿态"]
        data_res.sort(key=lambda d: d.id)
        items = self.pos_data.get_children()
        for i in items:
            self.pos_data.delete(i)
        for i in data_res:
            # self.pos_data.insert("", "end", value=[i.x + i.w / 2, i.y + i.h / 2, i.state])
            x_data.append(i.x + i.w / 2)
            y_data.append(i.y + i.h / 2)
            state_data.append(i.state)
        self.pos_data.insert("", "end", value=x_data)
        self.pos_data.insert("", "end", value=y_data)
        self.pos_data.insert("", "end", value=state_data)

    def img_op(self, op):
        def img_op_func():
            if self.img_loaded:
                tm.showinfo(title="开始标记", message="开始标记瓶盖")
                # self.img_dealer.filter_gray = self.filter_gray.get()
                op()
                tm.showinfo(title="标记完成", message="瓶盖标记完成！")
            else:
                self.no_img_error()

        return img_op_func

    def display_my_result(self, res):
        # if self.filter_gray.get():
        #     self.my_res = Image.fromarray(res)
        # else:
        #     self.my_res = Image.fromarray(res, mode="RGB")
        self.my_res = res
        my_res_display = ImageTk.PhotoImage(self.my_res.resize((600, 450), Image.ANTIALIAS))
        self.show_img(self.my_res_canvas, my_res_display)


app = AppGUI(1275, 700, "CV")
app.run()
