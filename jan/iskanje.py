import numpy as np
import re
from derivative import deriv3

# def iskanje3(x, n=100, tol=5):
#     data = branje(x)
#     frekvenca = np.zeros(len(data['Time']))
#     regex_vzorec = ["N.*_r"]
#
#     for i, vzorec in enumerate(regex_vzorec):
#         reg = re.compile(vzorec)
#         keys = list(filter(reg.match, data.keys()))
#         for j in range(len(frekvenca)):
#             for key in keys:
#                 frekvenca[j] = frekvenca[j] + data[key][j]
#
#     new_data = dict()
#     i = 0
#     mov_avg = 0
#     aktiven_dogodek = 0
#
#     while True:
#         if i >= n:
#             mov_avg += (frekvenca[i] - frekvenca[i - n]) / n
#             stdev = np.std(frekvenca[i - n: i])
#             if aktiven_dogodek >= n / 2:
#                 aktiven_dogodek = 0
#                 # regex_vzorec = ["N.*_u", "N.*_au", "N.*_i.*", "N.*_ai.*", "N.*_P.*", "N.*_Q.*", "N.*_f", "N.*_r"]
#                 # for k, vzorec in enumerate(regex_vzorec):
#                 #     reg = re.compile(vzorec)
#                 #     keys = list(filter(reg.match, data.keys()))
#                 for key in data.keys():
#                     new_data[key] = []
#                     for j in range(i - 1 - n, i - 1):
#                         new_data[key].append(data[key][j])
#                 i += 1
# #                print(i)
#                 yield new_data
#                 continue
#             elif aktiven_dogodek > 0:
#                 aktiven_dogodek += 1
#             elif abs(frekvenca[i + 1] - mov_avg) > tol * stdev and aktiven_dogodek == 0:
#                 aktiven_dogodek = 1
#
#         else:
#             mov_avg += frekvenca[i] / n
#
#         i += 1
#         if i >= len(data['Time']) - 1: break
#         yield 0

class iskanje():
    def __init__(self, n=100, tol=20, deriv=False):
        self.data = dict()
        self.frekvenca = []
        self.mov_avg = 0
        self.stdev = 0
        self.vsota = 0
        self.aktiven_dogodek = 0
        self.n = n
        self.tol = tol
        self.deriv = deriv

    def send_row(self, x):
        self.vsota = 0
        # doda nov element
        for key in self.data.keys():
            if key not in self.data:
                self.data[key] = []
            self.data[key].append(x[key])
        # odvaja frekvenco, ce ni v podatkih
        if self.deriv is False and len(self.data['Time']) >= 3:
            regex_vzorec = ["N.*_f"]
            for i, vzorec in enumerate(regex_vzorec):
                reg = re.compile(vzorec)
                keys = list(filter(reg.match, self.data.keys()))
                for key in keys:
                    self.vsota += deriv3(self.data[key][-3], self.data[key][-1])
                self.frekvenca.append(self.vsota)

        # sesteje odvode frekvence na vseh node-ih
        regex_vzorec = ["N.*_r"]
        for i, vzorec in enumerate(regex_vzorec):
            reg = re.compile(vzorec)
            keys = list(filter(reg.match, self.data.keys()))
            for key in keys:
                self.vsota += self.data[key][-2]
            self.frekvenca.append(self.vsota)

        if len(self.data['Time']) > self.n + 2:
            self.mov_avg += (self.frekvenca[-2] - self.frekvenca[0]) / self.n
            self.stdev = np.std(self.frekvenca[0:-2])
            for key in self.data.keys():
                self.data[key].pop(0)
            if self.aktiven_dogodek >= self.n / 2:
                self.aktiven_dogodek = 0
                return self.data, True
            elif self.aktiven_dogodek > 0:
                self.aktiven_dogodek += 1
                return self.data, False
            elif abs(self.frekvenca[-1] - self.mov_avg) > self.tol * self.stdev and self.aktiven_dogodek == 0:
                self.aktiven_dogodek = 1
                return self.data, False
        else:
            self.mov_avg += self.frekvenca[-1]
