#! /mip/opt/bin/python
import sys
from NumpyIm import *
import Image
import numpy as np
from scipy import misc 
from os.path import basename
#import matplotlib.image as mpimg
if (len(sys.argv)<3):
    print "convIm.py input.im slice#"
    sys.exit()

inim=sys.argv[1]
sliceNum=sys.argv[2]
data=ArrayFromIm(inim)
#slice1=data[sliceNum,:,:]
inim=basename(inim)
phanbase=inim[0:-3]
urnum=inim.strip().split('.')[1]

#print urnum[2:]
if int(urnum[2:]) >= 13 and int(urnum[2:]) <= 16:
   defloc='d1'
   lf='wl'
elif int(urnum[2:]) >= 1 and int(urnum[2:]) <= 4:
   defloc='d1'
   lf='nl'


if int(urnum[2:]) >= 17 and int(urnum[2:]) <= 20:
   defloc='d2'
   lf='wl'
elif int(urnum[2:]) >= 5 and int(urnum[2:]) <= 8:
   defloc='d2'
   lf='nl'

if int(urnum[2:]) >= 21 and int(urnum[2:]) <= 24:
   defloc='d3'
   lf='wl'
elif int(urnum[2:]) >= 9 and int(urnum[2:]) <= 12:
   defloc='d3'
   lf='nl'

#print defloc,lf


outim=[phanbase,'.',defloc,'.',lf,'.v',int(sliceNum)+1,'.png']
STR="".join([str(i) for i in outim])
print STR
misc.toimage(data[sliceNum,:,:], cmin=0.0, cmax=255.0).save(STR)
