#! /usr/bin/python
import csv 
import numpy

#define organ index 
medulla=1
bkg=2
cortex=0
spleen=3
kidney=4

m=numpy.loadtxt("/Users/Gary/Desktop/test.csv", delimiter=",",skiprows=1,usecols=(1,2,3,4,5))

#read patient index
output=[] 
n=open("/Users/Gary/Desktop/test.csv","rU")
for row in n:
 cells=row.strip().split(",")
 output.append(cells[0])
n.close()
print m[output.index('03Ma8c')-1,medulla]

