import numpy as np
from branje import branje
from iskanje import iskanje

def razlika(x):
    data = iskanje(x)
    delta_t = 1
    cas_dogodka = iskanje(x)[1]
    delta_i = delta_t / 0.02
    i_dogodka = cas_dogodka / 0.02
    
    regex_vzorec = ["N.*_P"]
    for i, vzorec in enumerate(regex_vzorec):
        reg = re.compile(vzorec)
        keys = list(filter(reg.match, data.keys()))
        for key in keys:
    
