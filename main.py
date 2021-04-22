from tkinter import *
import car_sensor as cs
import math as m
import fuzzy as fz
import os
import time
import numpy as np
import os.path

root = Tk()
w = Canvas(root, width=1000, height=1000)  # build the window


x0 = 40
y0 = 60
clength = 6
fix = 9
end_x0 = 0
end_y0 = 0
end_x1 = 0
end_y1 = 0
cx0 = 0
cy0 = 0
phi = 0


def fixx(x):
    return (x0 + x) * fix


def fixy(y):
    return (y0 - y) * fix


scriptpath = os.path.dirname(__file__)
inputpath = os.path.join(scriptpath, '..', 'src')
outputpath = os.path.join(scriptpath, '..', 'outputs')
filename = os.path.join(inputpath, 'case01.txt')
with open(filename) as f:
    c_x, c_y, c_deg = f.readline().split(",")
    end_x0, end_y0 = f.readline().split(",")
    end_x1, end_y1 = f.readline().split(",")
    x1, y1 = f.readline().split(",")
    x1 = float(x1)
    y1 = float(y1)
    end_x0 = float(end_x0)
    end_y0 = float(end_y0)
    end_x1 = float(end_x1)
    end_y1 = float(end_y1)
    cx0 = float(c_x)  # the original car center axis (cx0,cy0)
    cy0 = float(c_y)
    phi = float(c_deg)

    def line_line(x1, y1, x2, y2):  # 走道邊界
        return w.create_line(fixx(x1), fixy(y1), fixx(x2), fixy(y2), fill="blue", width=3)

    for line in f:
        x2, y2 = line.split(",")
        x2 = float(x2)
        y2 = float(y2)

        line_line(x1, y1, x2, y2)
        x1, y1 = x2, y2

  # draw the car and the line


def degtran(deg):
    return (m.pi / 180) * deg


def radtran(rad):
    return rad / (m.pi/180)


def my_car(cx, cy, phi, color):
    phi = degtran(phi)
    return w.create_oval(fixx(cx-3), fixy(3+cy), fixx(cx+3), fixy(-3+cy), outline=color, width=3),\
        w.create_line(fixx(cx), fixy(cy), fixx(clength * m.cos(phi) + cx),
                      fixy(clength * m.sin(phi) + cy), fill=color, width=3)  # phi已經先做過轉換了


def finish_line(x1, y1, x2, y2):
    return w.create_line(fixx(x1), fixy(y1), fixx(x2), fixy(y2), fill="red", width=3)


def start_line(x1, y1, x2, y2):
    return w.create_line(fixx(x1), fixy(y1), fixx(x2), fixy(y2), fill="black", width=3)


finish_line(end_x0, end_y0, end_x1, end_y1)
start_line(-12, 0, 12, 0)


# start moving
move_car, move_dir = my_car(cx0, cy0, phi, "red")  # move_car接圓, move_dir接車頭

train_4D_list = []
train_6D_list = []


def data_list(x, y, dm, dr, dl, theta):

    train_4D_list.append("%0.7f" % dm)  # 最小12位，7位小数
    train_4D_list.append("%0.7f" % dr)
    train_4D_list.append("%0.7f" % dl)
    train_4D_list.append("%0.7f" % theta)
    train_4D_list.append("\n")

    train_6D_list.append("%0.7f" % x)
    train_6D_list.append("%0.7f" % y)
    train_6D_list.append("%0.7f" % dm)
    train_6D_list.append("%0.7f" % dr)
    train_6D_list.append("%0.7f" % dl)
    train_6D_list.append("%0.7f" % theta)
    train_6D_list.append("\n")


def write_data():

    # f.write(str(i)) should be str
    data_txt = os.path.join(outputpath, 'train_4D.txt')
    f = open(data_txt, "w")
    f.write(" ")
    for i in train_4D_list:
        f.write(str(i))
        f.write(" ")

    data_txt = os.path.join(outputpath, 'train_6D.txt')
    f = open(data_txt, "w")
    f.write(" ")
    for i in train_6D_list:
        f.write(str(i))
        f.write(" ")


def hor_ang(phi, ang1):
    return phi - radtran(m.asin(2 * m.sin(degtran(ang1)) / clength))


def inv_check():
    data_txt = os.path.join(outputpath, 'train_6D.txt')
    with open(data_txt) as temp_f:

        # lines = temp_f.readline()
        x0, y0, m, r, l, ang = temp_f.readline().split()
        x0 = float(x0)
        y0 = float(y0)
        ang = float(ang)
        phi = 90
        move_car_r, move_dir_r = my_car(x0, y0, phi, "gray")

        for line in temp_f.readlines():

            x1, y1, m1, r1, l1, ang1 = line.split()
            x1 = float(x1)
            y1 = float(y1)
            ang1 = float(ang1)

            delta_x = x1 - x0
            delta_y = y1 - y0

            phi = hor_ang(phi, ang1)

            time.sleep(0.07)
            w.move(move_car_r, delta_x * fix, -delta_y * fix)

            w.coords(move_dir_r, fixx(x1), fixy(y1), fixx(
                clength * np.cos(degtran(phi)) + x1), fixy(clength * np.sin(degtran(phi)) + y1))

            x0, y0 = x1, y1
            w.update()


def movfunc():
    global cx0, cy0, phi
    if (cs.car_crash == False):
        global dm, dr, dl, theta
        dm = cs.d_sensor(cx0, cy0, phi)
        dr = cs.d_sensor(cx0, cy0, (phi - 45))
        dl = cs.d_sensor(cx0, cy0, (phi + 45))
        theta = fzy.get_theta(dm, dr, dl)  # degree in unit

        data_list(cx0, cy0, (dm + 3), (dr + 3), (dl + 3), theta)

        time.sleep(0.03)
        delta_x = m.cos(degtran(phi + theta)) + \
            m.sin(degtran(theta)) * m.sin(degtran(phi))
        delta_y = m.sin(degtran(phi + theta)) - \
            m.sin(degtran(theta)) * m.cos(degtran(phi))
        cx0 = cx0 + delta_x
        cy0 = cy0 + delta_y
        phi = phi - radtran(m.asin(2 * m.sin(degtran(theta)) / clength))

        w.move(move_car, delta_x * fix, -delta_y * fix)
        w.coords(move_dir, fixx(cx0), fixy(cy0), fixx(
            clength * m.cos(degtran(phi)) + cx0), fixy(clength * m.sin(degtran(phi)) + cy0))
        # 畫出軌跡
        finish_line(cx0, cy0, cx0 + 0.1, cy0 - 0.1)

        w.after(100, movfunc)

    else:
        data_list(cx0, cy0, (dm + 3), (dr + 3), (dl + 3), theta)  # 最後一筆資料
        write_data()
        # inv_check()


Button(root, text='ReadTxt', command=inv_check).pack()  # 按下按鈕讀取train_6D.txt
w.pack()

fzy = fz.fuzzy()
movfunc()
root.mainloop()
f.close()
