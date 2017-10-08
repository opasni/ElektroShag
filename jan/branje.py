import csv
import numpy as np
from datetime import datetime

def branje(x):
    arr = []
    ime = "../Data/" + x + ".csv"
    with open(ime) as dat_f:
        reader = csv.DictReader(dat_f, delimiter=";")
        for row in reader:
            arr.append(row)

    data = dict()
    time_arr = []
    for key in arr[0]:
        if key == 'Time':
            data[key] = []
        else:
            data[key] = np.zeros(len(arr))

    for i, line in enumerate(arr):
        for key in arr[0]:
            if key == 'Time':
                data[key].append(datetime.strptime(line[key], '%Y-%m-%d %H:%M:%S.%f'))
            else:
                try:
                    data[key][i] = float(line[key])
                except:
                    None

    return data
