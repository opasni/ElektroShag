import numpy as np
import re
from derivative import deriv3
from datetime import datetime


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
        for key in x.keys():
            if key not in self.data:
                self.data[key] = []
            if key == "Time":
                self.data[key].append(datetime.strptime(x[key], '%Y-%m-%d %H:%M:%S.%f'))
            else:
                try:
                    self.data[key].append(float(x[key]))
                except:
                    self.data[key].append(np.NaN)
        # odvaja frekvenco, ce ni v podatkih
        if self.deriv is False and len(self.data['Time']) >= 3:
            regex_vzorec = ["N.*_f"]
            for i, vzorec in enumerate(regex_vzorec):
                reg = re.compile(vzorec)
                keys = list(filter(reg.match, self.data.keys()))
                for key in keys:
                    self.vsota += deriv3(self.data[key][-3], self.data[key][-1])
                self.frekvenca.append(self.vsota)
        elif len(self.data["Time"]) > 1:
            # sesteje odvode frekvence na vseh node-ih
            regex_vzorec = ["N.*_r"]
            for i, vzorec in enumerate(regex_vzorec):
                reg = re.compile(vzorec)
                keys2 = list(filter(reg.match, self.data.keys()))
                for key2 in keys2:
                    self.vsota += self.data[key2][-2]
                self.frekvenca.append(self.vsota)

        if len(self.data['Time']) > self.n + 2:
            self.mov_avg = np.average(self.frekvenca[0:-2])  # (self.frekvenca[-2] - self.frekvenca[0]) / self.n
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
        elif len(self.frekvenca) > 0:
            self.mov_avg += self.frekvenca[-1]
        return self.data, False
