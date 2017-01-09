#! /usr/bin/python
import operator
x = [0, 7, 2, 4, 6, 9, 5]
y = [1, 2, 3, 4, 5, 6, 7]
print x,y,zip(x,y)
L = sorted(zip(x,y), key=operator.itemgetter(0))#to sort according to the 1st item in zip, use itemgetter(0)
new_x, new_y = zip(*L)
print new_x,new_y
