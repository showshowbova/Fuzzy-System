import numpy as np


class fuzzy:

    def get_theta(self, dm, dr, dl):
        drl = dr - dl

        dm_mu = []  # dm歸屬函數
        dm_mu.append(self.dm_s(dm))
        dm_mu.append(self.dm_m(dm))
        dm_mu.append(self.dm_l(dm))

        drl_mu = []  # dr - dl歸屬函數
        drl_mu.append(self.drl_s(drl))
        drl_mu.append(self.drl_m(drl))
        drl_mu.append(self.drl_l(drl))

        d_mu = []  # 取聯集歸屬函數
        mu_sums = 0
        theta_temp = 0

        con = [-15, 0, 15, -15, 0, 15, -15, 0, 15]  # 後鑑部 對照d_mu組合 小小, 小中, 小大

        for i in range(3):
            for j in range(3):
                d_mu.append(min(dm_mu[i], drl_mu[j]))

        for i in range(9):
            mu_sums = mu_sums + d_mu[i]
            theta_temp = (d_mu[i] * con[i]) + theta_temp
            # print(d_mu[i])

        theta = theta_temp / mu_sums
        theta = max(min(theta, 40), -40)
        return theta

    def dm_s(self, dm):
        y = 4 - dm
        if (dm < 3):
            return 1
        elif (dm <= 4):
            return y
        return 0

    def dm_l(self, dm):
        y = dm - 5
        if (dm > 6):
            return 1
        elif (dm >= 5):
            return y
        return 0

    def dm_m(self, dm):
        y1 = dm - 3
        y2 = 6 - dm
        if ((dm > 4) and (dm < 5)):
            return 1
        elif (dm >= 3) and (dm <= 5):
            return y1
        elif (dm >= 5) and (dm <= 6):
            return y2
        return 0

    def drl_s(self, drl):
        y = (-1 / 3) * drl - (1 / 3)
        if (drl < (-4)):
            return 1
        elif (drl <= (-1)):
            return y
        return 0

    def drl_l(self, drl):
        y = (1 / 3) * drl - (1 / 3)
        if (drl > 4):
            return 1
        elif (drl >= 1):
            return y
        return 0

    def drl_m(self, drl):
        y1 = (drl / 3) + (4 / 3)
        y2 = (4 / 3) - (drl / 3)
        if (drl > (-1)) and (drl < 1):
            return 1
        elif (drl >= (-4)) and (drl <= (-1)):
            return y1
        elif (drl >= 1) and (drl <= 4):
            return y2
        return 0


#fz_test = fuzzy()
#print(fz_test.get_theta(10, 4.485, 7.485))
