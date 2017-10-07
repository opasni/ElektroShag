import numpy as np
from branje import branje
import re

def iskanje2(x):
    data = branje(x)
    maks = 0
    cas = 0
    regex_vzorec = ["N.*_r"]
    for i, vzorec in enumerate(regex_vzorec):
        reg = re.compile(vzorec)
        keys = list(filter(reg.match, data.keys()))
        for key in keys:
            if np.amax(abs(data[key] - data[key][0])) > maks:
                maks = np.amax(abs(data[key]))
                cas = np.argmax(abs(data[key])) * 0.02

    return maks, cas

def iskanje(x, N = 50, tol = 0.02):
    data = branje(x)
    maks = 0
    cas = 0
    mov_avgs = []
    cumsum = [0]
    vsota = np.zeros(len(data['Time']))
    regex_vzorec = ["N.*_r"]
    
    for i, vzorec in enumerate(regex_vzorec):
        reg = re.compile(vzorec)
        keys = list(filter(reg.match, data.keys()))
        for j in range(len(vsota)):
            for key in keys:
                vsota[j] = vsota[j] + data[key][j]

    arr = []
    cumsum = [0]
    mov_avgs = []
    i = 1
    
    while True:
        cumsum.append(cumsum[i - 1] + vsota[i - 1])
        if i >= N:
            mov_avg = (cumsum[i] - cumsum[i - N] / N
            mov_avgs.append(mov_avg)
            if vsota[i + 1] > mov_avg and abs(vsota[i + 1] - mov_avg) > tol:
                aktiven_dogodek = True
                       # zacetek spikea, zacne delat array
            if vsota[i + 1] < mov_avg and abs(vsota[i + 1] - mov_avg) > tol:
                aktiven_dogodek = True
                       # po vrhu, array se dela naprej
            if abs(vsota[i + 1] - mov_avg) < tol and aktiven_dogodek = True:
                aktiven_dogodek = False
                return arr
        i = i + 1
            

