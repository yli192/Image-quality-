#! /mip/opt/bin/python
import sys, string
import os,subprocess
import numpy as np
from numpy import mat
from sys import exit, argv
from NumpyIm import ArrayFromIm, ArrayToIm
import scipy as sp
import math
import Image
from scipy import ndimage
if len(argv) != 5:
 	print "usage: extract.py coretx_phantom fbp_recon num_urs stacked_extracted_im"
        sys.exit(1)
raylen=70  #the length of the ray that is sent out from the center of mass of the cortex
WcortexIm=ArrayFromIm(argv[1])
reconIm=ArrayFromIm(argv[2])
reconIm=reconIm[0:(reconIm.shape[0]),0:(reconIm.shape[1]),0:(reconIm.shape[2]/2)] #extract only one kidney
num_urs=int(sys.argv[3])
outim=sys.argv[4]
absPath=os.path.abspath(argv[2])
splitted_absPath=absPath.split("/")
reconImBase=splitted_absPath[len(splitted_absPath)-1]
phanbase=reconImBase.split(".")[0]
urNum=int(reconImBase.split(".")[1][2:])

subset_sample_num=num_urs/6
up_normal_up=subset_sample_num #4
up_normal_low=1 #1
up_def_up=(subset_sample_num*4) # 16
up_def_low=(subset_sample_num*3)+1 # 13
lat_normal_up=subset_sample_num*2 #8
lat_normal_low=subset_sample_num+1 #5
lat_def_up=5*subset_sample_num 
lat_def_low=subset_sample_num*4+1
lp_normal_up=subset_sample_num*3
lp_normal_low=subset_sample_num*2+1
lp_def_up=num_urs
lp_def_low=subset_sample_num*5+1

if urNum <= up_def_up and urNum >= up_def_low or urNum <= up_normal_up and urNum >= up_normal_low:
 WCortexIm=WcortexIm.swapaxes(0,2)
 thetaindegree=270
elif  urNum <= lp_def_up and urNum >= lp_def_low or urNum <= lp_normal_up and urNum >=lp_normal_low :
 #print "enter 24-21,9-12"
 WCortexIm=WcortexIm.swapaxes(0,2)
 thetaindegree=90
elif urNum <= lat_def_up and urNum >= lat_def_low or urNum <= lat_normal_up and urNum >= lat_normal_low:
 WCortexIm=WcortexIm
 thetaindegree=180
#calculate dimensions of the image
LcortexIm=WcortexIm[0:(WcortexIm.shape[0]),0:(WcortexIm.shape[1]),0:(WcortexIm.shape[2]/2)]
if urNum <= up_def_up  and urNum >= up_def_low  or urNum <= lp_def_up and urNum >= lp_def_low or urNum <= up_normal_up and urNum >= up_normal_low or urNum <= lp_normal_up and urNum >= lp_normal_low:
 LCortexIm=LcortexIm.swapaxes(0,2)
 thetaindegree=90+thetaindegree
else:
 LCortexIm=LcortexIm
 thetaindegree=thetaindegree
theta=thetaindegree*np.pi/180
#here compute the com of one kidney, either left or right
com=ndimage.measurements.center_of_mass(WCortexIm) #center of mass of the whole kidney
lcom=ndimage.measurements.center_of_mass(LCortexIm) #center of mass of the left half kidney
#x,y,z below are coordinates of the com of the left kidney, which server as the start point of the ray
x=str(round(float(lcom[2]))) #need a string here
y=str(round(float(lcom[1]))) 
z=str(round(float(lcom[0])))
#determine end point of the ray
incrementx=raylen*np.cos(theta) #increment in x direction
incrementy=raylen*np.sin(theta) #increment in y direction
xend=str(round(float(lcom[2]))+incrementx) #  end x coordinate 
yend=str(round(float(lcom[1]))+incrementy) #  end y coordinate
#call improf
if urNum <= up_def_up  and urNum >= up_def_low  or urNum <= lp_def_up and urNum >= lp_def_low or urNum <= up_normal_up and urNum >= up_normal_low or urNum <= lp_normal_up and urNum >= lp_normal_low:
 #print "enter 9-12, 13-16,24-21,1-4"
 cmdimprof=['improf','-b',y,x,yend,xend,'-d',str(2),z,z,os.path.abspath(argv[1])] # everything inside must be a string, str(0) means in the z direction
#elif urNum <= 4 and urNum >=1 or  urNum <= 12 and urNum >=9:
# cmdimprof=['improf','-b',y,x,yend,xend,'-d',str(2),z,z,os.path.abspath(argv[1])]
elif urNum <= lat_def_up and urNum >=lat_def_low or urNum <= lat_normal_up and urNum >= lat_normal_low:
 #print "entering 5-8, 20-17"
 cmdimprof=['improf','-b',x,y,xend,yend,'-d',str(0),z,z,os.path.abspath(argv[1])] 

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
corthickness=u[outbd,0]-u[inbd,0]
raydistance=math.ceil(u[outbd,0]-(corthickness/2.0))
#print "raydistance to the outter cortical edge in units of pixels=",raydistance
comspherex=round(xint+raydistance*np.cos(theta))
comspherey=round(yint+raydistance*np.sin(theta))
comsphere=[comspherex,comspherey,zint]
# if the defect is lateral, need to switch x and z to make the corrdinate of the defect center in (z,y,x) order
#these are coordinate, namely pixel indexes, not total pixel numbers
if urNum <= lat_def_up and urNum >=lat_def_low or urNum <= lat_normal_up and urNum >= lat_normal_low:
 defCenter_x=int(round(comspherex/2))
 defCenter_y=int(round(comspherey/2))
 defCenter_z=int(round(zint/2))
else:
 defCenter_z=int(round(comspherex/2))
 defCenter_y=int(round(comspherey/2))
 defCenter_x=int(round(zint/2))
print "z:",defCenter_z,"y:",defCenter_y,"x:",defCenter_x
print "reconIm shape:",reconIm.shape
#half x,y,z coordinate
half_x=63
half_y=63
half_z=63
#now check if need to pad zeros given the center of the defect and the dimensions of the halved reconIm. If padding is needed, then how many zeros?
#zero padding check in the x direction
if defCenter_x - half_x <= 0 :
 increment_x=half_x-defCenter_x
 half_x=defCenter_x
elif reconIm.shape[2] < (defCenter_x+half_x):
 increment_x=defCenter_x+half_x-reconIm.shape[2]
 print "insufficient pixels in top x direction, increment_x:",increment_x
else: 
 increment_x=0
#zero padding check in the y direction
if defCenter_y - half_y <= 0:
 increment_y=half_y-defCenter_y
 half_y=defCenter_y
else:
 increment_y=0
#zero padding check in the z direction
if defCenter_z - half_z <= 0 and reconIm.shape[0] >= defCenter_z+64:
 increment_z=half_z-defCenter_z
 half_z=defCenter_z
 print "insufficient pixels in bottom z direction,increment_z:",increment_z
elif defCenter_z - half_z >= 0 and reconIm.shape[0] <= defCenter_z+64:
 increment_z=defCenter_z+half_z-reconIm.shape[0]
 print "insufficient pixels in top z direction,increment_z:",increment_z
elif defCenter_z - half_z <= 0 and reconIm.shape[0] <= defCenter_z+64:
 increment_z_bottom=half_z-defCenter_z
 increment_z_top=defCenter_z+half_z-reconIm.shape[0]
 increment_z=increment_z_top+increment_z_bottom
 half_z=defCenter_z
 print "insufficient pixels in both top and bottom z direction,increment_z_top,increment_z_bottom,increment_z:",increment_z_top,increment_z_bottom,increment_z
else:
 increment_z=0
print "increment_xyz:",increment_x,increment_y,increment_z
print "half_xyz:",half_x,half_y,half_z
#as half_xyz may have been changed above to take care of the lower bound so before extracting the images, need to reinitialize these values to take care of the image upper bound
half_x_init=64
half_y_init=64
half_z_init=64
#extrate the images from half of the reconstruction image (only one kidey)
coronalIm=reconIm[ (defCenter_z-half_z):(defCenter_z+half_z_init), defCenter_y , (defCenter_x-half_x):(defCenter_x+half_x_init) ]
sagittalIm=reconIm[(defCenter_z-half_z):(defCenter_z+half_z_init),(defCenter_y-half_y):(defCenter_y+half_y_init),defCenter_x]
transaxialIm=reconIm[defCenter_z,(defCenter_y-half_y):(defCenter_y+half_y_init),(defCenter_x-half_x):(defCenter_x+half_x_init)]

#before padding zeros
print "before padding"
print coronalIm.shape
print sagittalIm.shape
print transaxialIm.shape
#below are the coordinates of the defect center in the extracted images
new_defCenter_x=half_x # index starts from 0
new_defCenter_y=half_y
new_defCenter_z=half_z
new_coronalIm=np.zeros((128,128),np.float32)
new_sagittalIm=np.zeros((128,128),np.float32)
new_transaxialIm=np.zeros((128,128),np.float32)

#paste the extracted image to a 128x128 zero image and center the defect center at 63,63, note that coronalIm:(z,x), sagittalIm:(z,y), transaxialIm:(y,x)
offset_z=63-new_defCenter_z
offset_x=63-new_defCenter_x
offset_y=63-new_defCenter_y
print "offset_x_y_z:",offset_x, offset_y, offset_z
for i in range(coronalIm.shape[0]):
 for j in range(coronalIm.shape[1]):
  new_coronalIm[i+offset_z,j+offset_x]=coronalIm[i,j]
for i in range(sagittalIm.shape[0]):
 for j in range(sagittalIm.shape[1]):
  new_sagittalIm[i+offset_z,j+offset_y]=sagittalIm[i,j]
for i in range(transaxialIm.shape[0]):
 for j in range(transaxialIm.shape[1]):
  new_transaxialIm[i+offset_y,j+offset_x]=transaxialIm[i,j]
print "defect center pixel value:",reconIm[defCenter_z,defCenter_y,defCenter_x]
print "defect center pixel value in extracted coronal image:",new_coronalIm[63,63]
print "defect center pixel value in extracted sagittal image:",new_sagittalIm[63,63]
print "defect center pixel value in extracted transaxial image:",new_transaxialIm[63,63]
print "after padding"
print new_coronalIm.shape
print new_sagittalIm.shape
print new_transaxialIm.shape
stackedIm=np.dstack((new_coronalIm,new_sagittalIm,new_transaxialIm))
ffim=stackedIm.swapaxes(0,2)
ffim=ffim.swapaxes(1,2)
ArrayToIm(ffim,outim)




