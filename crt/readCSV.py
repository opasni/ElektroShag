import csv
import re
from collections import Counter

with open('data/Example_5B.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        print(row['Time'])
    #print(len(reader.fieldnames))
    print(reader.fieldnames[1])
    print(len(reader.fieldnames))
    x = []
    for i in range(1, len(reader.fieldnames)):
        nodeN= int("".join(i for i in reader.fieldnames[i].split("_")[0] if i.isdigit() or i == "."))
        x.append(nodeN)
        #powerlineN= int("".join(i for i in reader.fieldnames[i].split("_")[1] if i.isdigit() or i == "."))
    print(Counter(x).keys())
    print(Counter(x).values())
        #print(set(x))
        #print(reader.fieldnames[i][1])

print(reader.fieldnames)

import matplotlib.pyplot as plt
plt.plot(reader[0])

#import numpy as np

#myData = np.genfromtxt('Example_5B.csv', delimiter=';', names=True)

#print(myData["Time"])
#for name in myData.dtype.names:
#    print(myData[name])