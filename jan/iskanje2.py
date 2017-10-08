import numpy as np
from branje import branje
import re


def deriv3(xl, xr, h=0.02):
    """"
    Sprejme dve tocki oddaljeni za 2h, vrne vrednost na sredini!
    xl    tocka pri x-h
    xr    tocka pri x+h
    """
    return (xr - xl)/2/h


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


def iskanje(x, n=100, tol=5):
    data = branje(x)
    frekvenca = np.zeros(len(data['Time']))
    regex_vzorec = ["N.*_r"]

    for i, vzorec in enumerate(regex_vzorec):
        reg = re.compile(vzorec)
        keys = list(filter(reg.match, data.keys()))
        for j in range(len(frekvenca)):
            for key in keys:
                frekvenca[j] = frekvenca[j] + data[key][j]

    new_data = dict()
    i = 0
    mov_avg = 0
    aktiven_dogodek = 0

    while True:
        if i >= n:
            mov_avg += (frekvenca[i] - frekvenca[i - n]) / n
            stdev = np.std(frekvenca[i - n: i])
            if aktiven_dogodek >= n / 2:
                aktiven_dogodek = 0
                # regex_vzorec = ["N.*_u", "N.*_au", "N.*_i.*", "N.*_ai.*", "N.*_P.*", "N.*_Q.*", "N.*_f", "N.*_r"]
                # for k, vzorec in enumerate(regex_vzorec):
                #     reg = re.compile(vzorec)
                #     keys = list(filter(reg.match, data.keys()))
                for key in data.keys():
                    new_data[key] = []
                    for j in range(i - 1 - n, i - 1):
                        new_data[key].append(data[key][j])
                i += 1
#                print(i)
                yield new_data
                continue
            elif aktiven_dogodek > 0:
                aktiven_dogodek += 1
            elif abs(frekvenca[i + 1] - mov_avg) > tol * stdev and aktiven_dogodek == 0:
                aktiven_dogodek = 1

        else:
            mov_avg += frekvenca[i] / n

        i += 1
        if i >= len(data['Time']) - 1: break
        yield 0

