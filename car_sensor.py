import os
import math as m


def deg(deg):
    return (m.pi / 180) * deg


rad = 3
lo = []
le = []
inf_l = 1e5  # 無法抵達
inf_l = float(inf_l)
# line_x, line_yl, line_yh三點代表一垂直線
lo = [-6, -3, 22, 6, -3, 10, 18, 22, 50, 30, 10, 50]
# line_xl, line_xh, line_y三點代表一水平線 (xl,y) (xh,y)
le = [-6, 18, 22, 6, 30, 10, 18, 30, 50]
# 終點線(x1,y1) (x2,y2) xg1, yg1, xg2, yg2
final_point = [18, 40, 30, 37]
# 偵測是否撞牆或碰到終點
car_crash = False


def dis(x1, y1, x2, y2):
    return m.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def d_sensor(x1, y1, phi):  # x1 y1 車中心座標, x2 y2在圓周上
    phi = deg(phi)
    x2 = round(rad * m.cos(phi) + x1, 2)
    y2 = round(rad * m.sin(phi) + y1, 2)
    dh2 = dh4 = dh6 = d1 = d2 = d3 = d4 = d5 = d6 = d7 = inf_l

    is_goal(x1, y1, x2, y2,
            final_point[0], final_point[1], final_point[2], final_point[3])

    if x1 == x2:
        a = 1.0
        b = -x1
        x = x1
        dh2 = line_hor(x, y1, le[0], le[1], le[2])  # line2
        dh4 = line_hor(x, y1, le[3], le[4], le[5])  # line4
        dh6 = line_hor(x, y1, le[6], le[7], le[8])  # line6

    else:
        a = (y1 - y2) / (x1 - x2)  # 斜率
        b = y1 - (x1 * a)
        d1 = line_o(a, b, x1, y1, x2, y2, lo[0], lo[1], lo[2])  # line1
        d3 = line_o(a, b, x1, y1, x2, y2, lo[3], lo[4], lo[5])   # line3
        d5 = line_o(a, b, x1, y1, x2, y2, lo[6], lo[7], lo[8])  # line5
        d7 = line_o(a, b, x1, y1, x2, y2, lo[9], lo[10], lo[11])  # line7

        d2 = line_e(a, b, x1, y1, x2, y2, le[0], le[1], le[2])
        d4 = line_e(a, b, x1, y1, x2, y2, le[3], le[4], le[5])
        d6 = line_e(a, b, x1, y1, x2, y2, le[6], le[7], le[8])

    d = min(d1, d2, d3, d4, d5, d6, d7, dh2, dh4, dh6)
    return d


def compare(a, b, c, d, tarx, tary):
    xl = min(a, b)
    xh = max(a, b)
    yl = min(c, d)
    yh = max(c, d)
    if (tarx >= xl) and (tarx <= xh):
        if (tary >= yl) and (tary <= yh):
            return True
    return False

# 終點線必須非垂直線


def is_back(x, y, x1, y1, x2, y2, yg1, yg2):
    global car_crash
    if y >= yg2 and y <= yg1:
        d_c2l = dis(x, y, x1, y1)
        if (not compare(x, x1, y, y1, x2, y2)):  # 交點是否在正後方
            if (d_c2l > (rad + 2)):
                car_crash = True


def is_goal(x1, y1, x2, y2, xg1, yg1, xg2, yg2):
    a_g = (yg1 - yg2) / (xg1 - xg2)  # 斜率
    b_g = yg1 - (xg1 * a_g)
    if x1 == x2:
        x = x1
        y = (a_g * x1 + b_g)  # 與終點線的交點
        is_back(x, y, x1, y1, x2, y2, yg1, yg2)
    else:
        a = (y1 - y2) / (x1 - x2)  # 車斜率
        b = y1 - (x1 * a)
        if a != a_g:
            x = (b - b_g) / (a_g - a)
            y = a * x + b
            is_back(x, y, x1, y1, x2, y2, yg1, yg2)


def line_o(a, b, x1, y1, x2, y2, line_x, line_yl, line_yh):  # 計算垂直牆到車正面距離
    y = (a * line_x) + b  # x, y為交點
    x = line_x
    global car_crash  # use global variable
    if y >= line_yl and y <= line_yh:  # 與走道有交點
        d_c2l = dis(x, y, x1, y1)  # 圓心到line1的距離
        if (compare(x, x1, y, y1, x2, y2)):  # 交點是否在正前方
            return round((d_c2l - rad), 7)  # 車到line1的距離
        elif (d_c2l < rad):
            car_crash = True
            return inf_l
    return inf_l


def line_e(a, b, x1, y1, x2, y2, line_xl, line_xh, line_y):
    if a != 0:  # 若為水平線則不可能有交集
        y = line_y
        x = (y - b) / a
        d_c2l = dis(x, y, x1, y1)
        global car_crash
        if x >= line_xl and x <= line_xh:
            if (compare(x, x1, y, y1, x2, y2)):
                return round((d_c2l - rad), 7)
            elif (d_c2l < rad):
                car_crash = True
                return inf_l
    return inf_l

# 偶數line紀錄水平邊界 line_xl, line_xh, line_y是邊界的x y 座標


def line_hor(x, y, line_xl, line_xh, line_y):  # x y為圓心
    global car_crash
    if (line_y - y) >= rad:
        if x >= line_xl and x <= line_xh:
            return round(((line_y - y) - rad), 7)
    elif ((line_y - y) >= 0):  # 交點到圓心距離小於半徑
        car_crash = True
        return inf_l
    return inf_l


def finish_l(a, b, x1, y1, x2, y2, line_x, line_yl, line_yh):  # 計算垂直牆到車正面距離
    y = (a * line_x) + b  # x, y為交點
    x = line_x
    global car_crash  # use global variable
    if y >= line_yl and y <= line_yh:  # 與走道有交點
        d_c2l = dis(x, y, x1, y1)  # 圓心到line1的距離
        if (compare(x, x1, y, y1, x2, y2)):  # 交點是否在正前方
            return round((d_c2l - rad), 7)  # 車到line1的距離
        elif (d_c2l < rad):
            car_crash = True
            return inf_l
    return inf_l


# print(d_sensor(12, 18, 135))  # TEST 偶數 2.6568542
# print(d_sensor(5, 0, 45))  # TEST car_crash = true
# print(d_sensor(0, 20, 90))  # TEST line_hor car_crash = true
# print(d_sensor(0, -1, 90))  # TEST line_hor car_crash = False
# print(car_crash)
