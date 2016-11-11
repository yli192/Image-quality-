#! /mip/opt/bin/python
import sys, string
import os,subprocess
import numpy as np
from numpy import mat
from sys import exit, argv
from NumpyIm import ArrayFromIm, ArrayToIm
import scipy as sp
import math
from scipy import ndimage
if len(argv) != 4:
 	print "usage: extract.py coretx_phantom fbp_recon stacked_extracted_im"
        sys.exit(1)
raylen=70  #the length of the ray that is being sent out from the com of the cortex
WcortexIm=ArrayFromIm(argv[1])
reconIm=ArrayFromIm(argv[2])
outim=sys.argv[3]
absPath=os.path.abspath(argv[2])
splitted_absPath=absPath.split("/")
reconImBase=splitted_absPath[len(splitted_absPath)-1]
phanbase=reconImBase.split(".")[0]
urNum=int(reconImBase.split(".")[1][2:])
print phanbase,urNum
#if argv[1] == "-s" :
if urNum <= 16 and urNum >=13 or urNum <= 4 and urNum >=1:
 WCortexIm=WcortexIm.swapaxes(0,2)
 thetaindegree=270
elif  urNum <= 24 and urNum >=21 or urNum <= 8 and urNum >=5 :
 WCortexIm=WcortexIm.swapaxes(0,2)
 thetaindegree=90
## print "sagital"
#elif argv[1] =="-l":
elif urNum <= 20 and urNum >=17 or urNum <= 12 and urNum >=9:
 WCortexIm=WcortexIm
 thetaindegree=180
##here need to know dimension of the image
LcortexIm=WcortexIm[0:(WcortexIm.shape[0]),0:(WcortexIm.shape[1]),0:(WcortexIm.shape[2]/2)]
#if argv[1] == "-s" :
if urNum <= 16 and urNum >=13 or urNum <= 24 and urNum >=21 :
 LCortexIm=LcortexIm.swapaxes(0,2)
#elif argv[1] =="-l":
elif urNum <= 20 and urNum >=17 :
 LCortexIm=LcortexIm
##image=im.swapaxes(2,0)
#thetaindegree=float(argv[3])
#if argv[1] == "-s" :
if urNum <= 16 and urNum >=13 or urNum <= 24 and urNum >=21:
 thetaindegree=90+thetaindegree
#elif argv[1] =="-l":
elif urNum <= 20 and urNum >=17 :
 thetaindegree=thetaindegree
theta=thetaindegree*np.pi/180
##defvol=float(argv[4])
##sphereim=sys.argv[5]
##outim=sys.argv[6]
#
##here you want to compute the com of one kidney, either left or right
com=ndimage.measurements.center_of_mass(WCortexIm) #center of mass of the whole kidney
lcom=ndimage.measurements.center_of_mass(LCortexIm) #center of mass of the left half kidney
#x,y,z below are coordinates of the com of the left kidney, which server as the start point of the ray
x=str(round(float(lcom[2]))) #must be a string 
y=str(round(float(lcom[1]))) 
z=str(round(float(lcom[0])))
##if argv[1] == "-l" :
## print "ray starting point coordinate (x,y,z)=",x,y,z
##elif argv[1] == "-s" :
## print "ray starting point coordinate (x,y,z)=",z,y,x
## determine end point of the ray
incrementx=raylen*np.cos(theta) #increment in x direction
incrementy=raylen*np.sin(theta) #increment in y direction
#incrementz=raylen*np.sin(theta) #increment in z direction
xend=str(round(float(lcom[2]))+incrementx) #  end x coordinate 
yend=str(round(float(lcom[1]))+incrementy) #  end y coordinate
#zend=str(round(float(lcom[0]))+incrementz) #  end y coordinate
##call improf
#if argv[1] == "-s" :
if urNum <= 16 and urNum >=13 or urNum <= 24 and urNum >=21:
 print 1
 cmdimprof=['improf','-b',y,x,yend,xend,'-d',str(2),z,z,os.path.abspath(argv[1])] # everything inside must be a string, str(0) means in z direction
#elif argv[1] == "-l" :
elif urNum <= 20 and urNum >=17 :
 cmdimprof=['improf','-b',x,y,xend,yend,'-d',str(0),z,z,os.path.abspath(argv[1])] # everything inside must be a string, str(0) means in z direction
improfout=subprocess.check_output(cmdimprof) 
newimprofout=improfout[improfout.index('\n')+1:] #skip reading the first row of improfout
b=mat(newimprofout) #a 1d matrix of improf output
u=b.reshape(b.shape[1]/2,2) # reshape b to get a N*2 matrix 
for i in range(u.shape[0]-1):
  if u[i,1]-u[i+1,1]==-1:
	inbd=i+1 
  elif u[i,1]-u[i+1,1]==1:
	outbd=i
xint=round(float(lcom[2]))
yint=round(float(lcom[1]))
zint=round(float(lcom[0])) 
#print inbd,outbd
corthickness=u[outbd,0]-u[inbd,0]+1
#print "cortex thickness in units of pixels=",corthickness
##raydistance=(u[outbd,0]+u[inbd,0])/2
raydistance=u[outbd,0]
##print raydistance
##print "raydistance to the outter cortical edge in units of pixels=",raydistance
comspherex=round(xint+raydistance*np.cos(theta))
comspherey=round(yint+raydistance*np.sin(theta))
comsphere=[comspherex,comspherey,zint]
print "comsphere:",comsphere

int_x=int(round(comspherex/2))
int_y=int(round(comspherey/2))
int_z=int(round(zint/2))
print "x:",int_x,"y:",int_y,"z:",int_z
print "reconIm shape:",reconIm.shape
#takes care of sphere centered at less than 32
half_size_x=32
half_size_y=32
half_size_z=32
if urNum <= 16 and urNum >=13 or urNum <= 24 and urNum >=21:
 if int_x < half_size_x:
  increment_x=half_size_x-int_x
  half_size_x=int_x
 elif reconIm.shape[0] < int_x+half_size_x:
  increment_x=int_x+half_size_x-reconIm.shape[0]
 elif int_y <= half_size_y:
  increment_y=half_size_y-int_y
  half_size_y=int_y
 elif int_z <= half_size_z:
  increment_z=half_size_z-int_z
  half_size_z=int_z
 else:
  increment_x=increment_y=increment_z=0
else:
 increment_x=increment_y=increment_z=0
 print "lateral defect"
#print "increment_xyz:",increment_x,increment_y,increment_z
if urNum <= 16 and urNum >=13 or urNum <= 24 and urNum >=21:
 coronalIm=reconIm[ (int_x-half_size_x):(int_x+half_size_x), int_y , (int_z-half_size_z):(int_z+half_size_z) ]
#sagittal
 sagittalIm=reconIm[(int_x-half_size_x):(int_x+half_size_x),(int_y-half_size_y):(int_y+half_size_y),int_z]
#transaxial
 transaxialIm=reconIm[int_x,(int_y-half_size_y):(int_y+half_size_y),(int_z-half_size_z):(int_z+half_size_z)]
elif  urNum <= 20 and urNum >=17 :
 coronalIm=reconIm[ (int_z-half_size_z):(int_z+half_size_z), int_y , (int_x-half_size_x):(int_x+half_size_x) ]
 sagittalIm=reconIm[(int_z-half_size_z):(int_z+half_size_z),(int_y-half_size_y):(int_y+half_size_y),int_x]
 transaxialIm=reconIm[int_z,(int_y-half_size_y):(int_y+half_size_y),(int_x-half_size_x):(int_x+half_size_x)]

if increment_x !=0 and half_size_x !=32:
 coronalIm = np.pad(coronalIm, ((increment_x,increment_x),(0,0)), mode='constant')# "((add n rows above it,n rows below it),(n cols to the left of it, n cols to the right of it))"
 sagittalIm = np.pad(sagittalIm, ((increment_x,increment_x),(0,0)), mode='constant')
elif increment_x !=0 and half_size_x ==32:
 coronalIm = np.pad(coronalIm, ((increment_x,0),(0,0)), mode='constant')# "((add n rows above it,n rows below it),(n cols to the left of it, n cols to the right of it))"
 sagittalIm = np.pad(sagittalIm, ((increment_x,0),(0,0)), mode='constant')
elif increment_z !=0 :
 coronalIm = np.pad(coronalIm, ((increment_z,increment_z),(0,0)), mode='constant')# "((add n rows above it,n rows below it),(n cols to the left of it, n cols to the right of it))"
 sagittalIm = np.pad(sagittalIm, ((increment_z,increment_z),(0,0)), mode='constant')
else:
 print "no need to pad zero"
print coronalIm.shape
print sagittalIm.shape
print transaxialIm.shape

stackedIm=np.dstack((coronalIm,sagittalIm,transaxialIm))
ffim=stackedIm.swapaxes(0,2)
ffim=ffim.swapaxes(1,2)
ArrayToIm(ffim,outim)




