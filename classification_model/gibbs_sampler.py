#! /Users/Gary/anaconda2/bin/python

import numpy as np
import matplotlib.pyplot as plt
from numpy import random
#from scipy import misc
import skimage.color
im = plt.imread('cat3.jpg')
#plt.imshow(im)
#plt.show()
#import skimage.color
def myimshow(state):
    plt.imshow(state,interpolation='nearest')

def preproc_data(im,scale=0.2,debug=False):
    import skimage.color
    import skimage.transform

    tinyim = skimage.transform.rescale(im,scale)
    grayim = skimage.color.rgb2gray(tinyim)

    scale = grayim.max() - grayim.min()
    data = 2 * (grayim - grayim.min()) / scale - 1

    if debug:
        print 'original range:', grayim.min(), grayim.max()
        print 'remapped range:', data.min(), data.max()

    return [data,tinyim]

[data,im] = preproc_data(im,debug=True)
#plt.figure()
#plt.imshow(im) # image is now downsampled
#plt.figure()
#plt.imshow(data)
#plt.show()
def getneighor(y, x, h, w): # get 4-side neighbor
    n = []
    if (x != 0): n.append((y, x-1))
    if (x != w-1): n.append((y, x+1))
    if (y != 0): n.append((y-1, x))
    if (y != h-1): n.append((y+1, x))
    return n

def poslist(h,w):
    '''Get point list of a grid'''
    pos = []
    for x in range(w):
        for y in range(h):
            pos.append((y, x))
    return pos

def energy_prior(state, gamma):
    total = 0
    (h, w) = state.shape
    pos = poslist(h, w)
    for p in pos:
        neighbor = getneighor(p[0], p[1], h, w) # compute neighbor

        for n in neighbor:
            total += state[p[0]][p[1]] * state[n[0]][n[1]]
    E = - gamma * total
    return E

def energy_data(state, data, eta):
    E = eta * sum((data - state)**2)
    return E

def energy(state, data, gamma, eta):
    return energy_prior(state, gamma) + energy_data(state, data, eta)

def gibbs_sampler(state, data, gamma, eta, debug=False): # 0/1 state
    (h, w) = state.shape
    new_state = state.copy()
    pos = poslist(h, w)
    for p in pos:
        neighbor_pos = getneighor(p[0], p[1], h, w)
        neighbor_value = [new_state[n[0]][n[1]] for n in neighbor_pos]

        tmp1 = -gamma * -1 * sum(neighbor_value) # x_i = -1
        tmp2 = -gamma * 1 * sum(neighbor_value) # x_i = 1

        # add data term
        v = data[p[0]][p[1]]
        tmp1 += eta * (v - (-1))**2 # x_i = -1
        tmp2 += eta * (v - 1)**2 #  x_i = 1

        tmp1 = np.exp(-tmp1)
        tmp2 = np.exp(-tmp2)

        p1 = tmp1 / (tmp1 + tmp2)
        prob = random.uniform() # roll a dice

        if (debug): print p1
        if (prob > p1):
            new_state[p[0]][p[1]] = 1
        else:
            new_state[p[0]][p[1]] = -1
    return new_state

from IPython.display import display, clear_output
import time

random_seed = 1 # Change this in your experiment
random.seed(random_seed)

(h, w) = data.shape
mat = random.random((h,w))
mat[mat>0.5] = 1
mat[mat<=0.5] = -1
random_state = mat

# Initial the random state
init_state = random_state

# Set parameters
gamma = 0.5
eta = 1

new_state = random_state.copy()
E = [energy(init_state, data, gamma, eta)] # array of energies at each iteration

f, ax = plt.subplots() # prepare animation
for i in range(60):
    clear_output(wait=True)
    new_state = gibbs_sampler(new_state, data, gamma, eta)
    E.append(energy(new_state, data, gamma, eta))

    # time.sleep(1)
    myimshow(new_state)
    display(f)
    #plt.show()
plt.title("Foreground")
mask = (new_state==1)
fg = im.copy()
#plt.imshow(mask)
for i in range(3):
    fg[:,:,i] = fg[:,:,i] * mask
plt.imshow(fg, cmap='gray', interpolation='nearest')
plt.figure()
plt.plot(range(61),E) ;plt.ylabel('energy function')
plt.show()
