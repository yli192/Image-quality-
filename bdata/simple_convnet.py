#! /usr/bin/python
import numpy as np
X = np.array([ [0,0,1],[0,1,1],[1,0,1],[1,1,1]]) # 4 by 3
y = np.array([[0,1,1,0]]).T #transpose these are the classes[ 0 1 1 0] that corresponde to [0 0 1] [ 0 1 1 ], etc

w0 = 2*np.random.random((3,4)) - 1
w1 = 2*np.random.random((4,1)) - 1

for j in xrange(60000):
 l1 = 1/(1+np.exp(-(np.dot(X,w0)))) #gate 1; work done in layer 1; activation fucntion in layer 1; 4 by 4
 l2 = 1/(1+np.exp(-(np.dot(l1,w1)))) # 4 by 1
 l2_delta = (y - l2)*(l2*(1-l2)) # updates(error weighted derivatives[error* slope]) on w1, the weights between l1 and l2; (l2*(1-l2)) is simply the gradient of the sigmod function. diff in caffe; still a 4 by 1 vector
 l1_delta = l2_delta.dot(w1.T) * (l1 * (1-l1)) # propagating error from the very end, namely (y-l2) back up the chain and multiply this error with slope of sigmod in l1
 w1 += l1.T.dot(l2_delta) # input from l1 * l2_delta
 w0 += X.T.dot(l1_delta) #input * l1_delta
 #print l2_delta
#now use the trained cnn on a tesing data
X_test = np.array([ [0,0,1],[1,1,1],[1,0,1],[1,1,1]])
#X_test = X
l1 = 1/(1+np.exp(-(np.dot(X_test,w0))))
l2 = 1/(1+np.exp(-(np.dot(l1,w1))))
print l2
