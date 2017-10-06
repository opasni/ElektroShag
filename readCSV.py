import csv
with open('Example_5B.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        print(row['Time'])
    print(len(reader.fieldnames))
        


#import numpy as np

#myData = np.genfromtxt('Example_5B.csv', delimiter=';', names=True)

#print(myData["Time"])
#for name in myData.dtype.names:
#    print(myData[name])