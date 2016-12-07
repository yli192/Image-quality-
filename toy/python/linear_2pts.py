#! /usr/bin/python

from numpy import ones,vstack
from numpy.linalg import lstsq
points = [(30,0.7634),(50,0.9040)]
x_coords, y_coords = zip(*points)
A = vstack([x_coords,ones(len(x_coords))]).T
m, c = lstsq(A, y_coords)[0]
print "Line Solution is y = {m}x + {c}".format(m=m,c=c)
