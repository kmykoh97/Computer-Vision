from PIL import Image
import numpy as np
import math
import cv2
import os.path


class CapUnit:
    x = 0
    y = 0
    w = 0
    h = 0
    bw = 0
    bh = 0
    id = 0
    state = "正"

    def __init__(self, x, y, w, h, bw, bh, id):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bw = bw
        self.bh = bh
        self.id = id

    def get_unit(self, img):
        return np.copy(img[self.y:self.y + self.h, self.x:self.x + self.w])

    def get_name(self):
        return "cap_unit_" + str(self.id) + ".jpg"

    def mark_cap(self, img):
        rec_color = (0, 150, 0)
        if self.state == "正":
            rec_color = (200, 0, 0)
        elif self.state == "立":
            rec_color = (0, 0, 200)
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), rec_color, 2)
        cv2.putText(img, str(self.id), (self.x, self.y - 1), cv2.FONT_HERSHEY_COMPLEX, 3, rec_color, 2)

    def set_state(self, state):
        self.state = state


class BottleCapDealer:
    img_name = ""
    img_self_name = ""
    img_pil = 0
    img_data = 0
    img_show = 0
    img_gray = 0
    img_binary = 0
    img_parent_path = ""
    caps = []
    standing_caps = []
    up_caps = []
    down_caps = []

    def read_img(self, img_name):
        self.img_name = img_name
        self.img_data = cv2.imread(img_name)
        self.img_pil = Image.fromarray(cv2.cvtColor(self.img_data, cv2.COLOR_RGB2BGR), mode="RGB")
        self.img_gray = cv2.cvtColor(self.img_data, cv2.COLOR_BGR2GRAY)
        self.img_parent_path, self.img_self_name = os.path.split(self.img_name)
        self.caps = []
        print(self.img_data.shape)

    # 这里为处理过程，res为结果图像
    def dealing_process(self):
        res = np.copy(self.img_data)
        ret, self.img_binary = cv2.threshold(self.img_gray, 20, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(self.img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#        cv2.imshow("circles", self.img_binary)
        caps = []
        i = 0
        for itc in contours:
            box_pos, box_shape, box_angle = cv2.minAreaRect(itc)
            x, y, w, h = cv2.boundingRect(itc)
            if box_shape[0] > 210 and box_shape[1] > 210:
                i = i + 1
                print(box_shape)
                print((w, h))
                # cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)
                caps.append(CapUnit(x, y, w, h, box_shape[0], box_shape[1], i))
        for scan in caps:
            self.handle_each_cap(scan)
        for scan in self.caps:
            scan.mark_cap(res)
        self.save_img("cap_detect_result.jpg", res)
        self.save_img("cap_binary.jpg", self.img_binary)
        return Image.fromarray(cv2.cvtColor(res, cv2.COLOR_RGB2BGR), mode="RGB"), self.caps

    def handle_each_cap(self, unit):
        cap_unit = unit.get_unit(self.img_data)
        check = self.check_pre(cap_unit)
        if abs(unit.bh - unit.bw) > 100 or self.check_standing(check):
            unit.state = "立"
            self.caps.append(unit)
            self.standing_caps.append(unit)
        elif self.check_front(check):
            unit.state = "正"
            self.caps.append(unit)
        else:
            unit.state = "反"
            self.caps.append(unit)
        return cap_unit

    def check_pre(self, check_cap):
        check_temp = np.copy(check_cap)
        check_temp = cv2.medianBlur(check_temp, 5)
        check_temp = cv2.cvtColor(check_temp, cv2.COLOR_RGB2GRAY)
        check_temp = cv2.GaussianBlur(check_temp, (9, 9), 2)
        check_temp = cv2.Canny(check_temp, threshold1=100, threshold2=200, apertureSize=5)
        return check_temp

    def check_standing(self, check_cap):
        # if abs(check_cap.shape[0] - check_cap.shape[1]) > 100:
        #     return True
        check_temp = np.copy(check_cap)
        # check_temp = cv2.medianBlur(check_temp, 5)
        # check_temp = cv2.cvtColor(check_temp, cv2.COLOR_RGB2GRAY)
        # check_temp = cv2.GaussianBlur(check_temp, (9, 9), 2)
        # check_temp = cv2.Canny(check_temp, threshold1=100, threshold2=200, apertureSize=5)
        circles = cv2.HoughCircles(check_temp, cv2.HOUGH_GRADIENT, dp=1, minDist=800, param1=200, param2=40,
                                   minRadius=150, maxRadius=500)
        print(circles)
        if circles is None:
            return True
        circles = np.uint16(np.around(circles))
        # check_temp = cv2.cvtColor(check_temp, cv2.COLOR_GRAY2BGR)
        # for c in circles[0, :]:
        #    check_temp = cv2.circle(check_temp, (c[0], c[1]), c[2], (255, 0, 0), 2)
        return False

    def check_front(self, check_cap):
        # 判断是否为正面，是的话返回True
        # check_cap为传入的一个瓶盖的小图
        check_temp = np.copy(check_cap)
        circles = cv2.HoughCircles(check_temp, cv2.HOUGH_GRADIENT, dp=1, minDist=5)
        if circles is None or circles.shape[1] < 130:
            return True
        # print(circles.shape)
        return False

    def save_img(self, save_name, save_data):
        cv2.imwrite(self.img_parent_path + "/" + save_name, save_data)

#    def find_caps(self):
