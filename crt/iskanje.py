import numpy as np
from branje import branje
import re

def iskanje(x):
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

