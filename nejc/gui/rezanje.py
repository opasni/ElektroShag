import numpy as np
import re
from branje import branje
from iskanje import iskanje

def rezanje(x):
    data = branje(x)
    delta_t = 1
    cas_dogodka = iskanje(x)[1]
    delta_i = delta_t * 50
    i_dogodka = cas_dogodka * 50
    new_data = dict()
    
    # regex_vzorec = ["N.*_u", "N.*_au", "N.*_i.*", "N.*_ai.*", "N.*_P.*", "N.*_Q.*", "N.*_f", "N.*_r"]
    regex_vzorec = ["N.*_P", "N.*i"]
    for i, vzorec in enumerate(regex_vzorec):
        reg = re.compile(vzorec)
        keys = list(filter(reg.match, data.keys()))
        for key in keys:
            new_data[key] = np.ndarray(int(2 * delta_i - 1))
            k = 0
            for j in range(len(data[key])):
                if abs(i_dogodka - j) < delta_i:
                    new_data[key][k] = data[key][j]
                    k = k + 1

    return new_data