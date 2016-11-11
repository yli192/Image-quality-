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
def RotateAxes(x,y,z,thetas):
   # thetas is an array of Euler angles (in radians) describing rotation about 
        # the x, rotated y, and rotate z axes. Note that this is not the 'normal'
        # Euler convention, but is a so-called Tait-Bryan convention (see Wikipedia
        # article on Euler Angles).
        axes=sp.array(((0,0,1),(0,1,0),(1,0,0))) # axes of rotation in order applied
        rm=sp.identity(3) # rm is rotation matrix. Starts as identity
        for i in range(3):
                if thetas[i] != 0: # no need to rotate if angle is 0
                        rm = sp.dot(RotationMatrix3D(thetas[i],axes[i]),rm)
        # 'dot' function is matrix multiplcation. Broadcasting rules make
        # it works on stacked triples of coordinates resulting from vstack function
        coords=sp.vstack((x.flatten(),y.flatten(),z.flatten()))
        rotcoords=sp.dot(rm,coords)
        return rotcoords[0].reshape(x.shape), rotcoords[1].reshape(y.shape),\
                rotcoords[2].reshape(z.shape)

def MakeEllipsoid(dims,pixsize,center,sphere_radius,corthickness):
    size=[sphere_radius,sphere_radius,corthickness*pixsize]
    #center=[0,0,0]
    rotation=[0,0,0]
    #print comspherex
    #center=[(zint-0.5*dims[0]+0.5)*pixsize,(comspherey-0.5*dims[1]+0.5)*pixsize,(comspherex-0.5*dims[2]+0.5)*pixsize]
    #print "  ellipsoid: size=",size, ", center= ",center
    z,y,x=sp.mgrid[0:dims[0],0:dims[1],0:dims[2]]
    z=(z-(dims[0]-1)*0.5)*pixsize
    y=(y-(dims[1]-1)*0.5)*pixsize
    x=(x-(dims[2]-1)*0.5)*pixsize
    xr,yr,zr=RotateAxes((x-center[2]),(y-center[1]), (z-center[0]),rotation)
    #print xr-x,yr-y,zr-z
    r=((xr/size[2])**2 + (yr/size[1])**2 +(zr/size[0])**2) 
    out=(r <= 1.0).astype(sp.float32)
    #print '      voxels=',out.sum(), 'analytic volume=',\
    #       sp.pi*4.0/3.0*(size[0]*size[1]*size[2])/pixsize**3
    return out

def ReadIm(args):
	WcortexIm=ArrayFromIm(argv[2])
        if argv[1] == "-s" :
         WCortexIm=WcortexIm.swapaxes(0,2)
        # print "sagital"
        elif argv[1] =="-l":
         WCortexIm=WcortexIm
        #here need to know dimension of the image
        LcortexIm=WcortexIm[0:(WcortexIm.shape[0]),0:(WcortexIm.shape[1]),0:(WcortexIm.shape[2]/2)]
        if argv[1] == "-s" :
         LCortexIm=LcortexIm.swapaxes(0,2)
        elif argv[1] =="-l" :
         LCortexIm=LcortexIm
        #image=im.swapaxes(2,0)
        thetaindegree=float(argv[3])
        if argv[1] == "-s" :
         thetaindegree=90+thetaindegree
        elif argv[1] =="-l" :
         thetaindegree=thetaindegree
        theta=thetaindegree*np.pi/180
        defvol=float(argv[4])
        sphereim=sys.argv[5]
        outim=sys.argv[6]
	return LCortexIm, WCortexIm, theta, defvol, sphereim, outim

def findIntersecs(u):
	for i in range(u.shape[0]-1):
          if u[i,1]-u[i+1,1]==-1:
                inbd=i+1
          elif u[i,1]-u[i+1,1]==1:
                outbd=i
	return inbd,outbd

def findOptSphere(defvol,delta,intersec_vol_current,sphere_radius_current,dims,pixsize,center,sphere_radius,corthickness,WCortexIm):
	for j in range(30):  #iter#=30
		if intersec_vol_current <= defvol :
			delta = abs(delta)
		else:
			delta= -abs(delta)
		print "delta to be tested,",delta
		#sphere_radius=sphere_radius_current
		sphere_radius=sphere_radius_current+delta
		print "sphere_radius to be tested=", sphere_radius
		sphere_test=MakeEllipsoid(dims,pixsize,center,sphere_radius,corthickness)
		intersection_test=sphere_test*WCortexIm
		intersec_vol_test=intersection_test.sum()
		if abs(intersec_vol_test-defvol) <= 3 or j==29: #give up when error is witnin 3 voxels or at the 29th iteration or converged
		   if   abs(intersec_vol_test-defvol) <= abs(intersec_vol_current-defvol):
			sphere_radius_final=sphere_radius
		   elif j == 0: #lucky case: enter this loop in its first iter 
			sphere_radius_final=sphere_radius
		   else:
			sphere_radius_final=sphere_radius_current
		   delta_final=delta
		   print "final sphere size found=",sphere_radius_final
		   print "final inter_sec_vol=",intersec_vol_test
		   break
		elif intersec_vol_test > intersec_vol_current and intersec_vol_test < defvol or abs(intersec_vol_test-defvol) <= 10: 
		 print "intersect_vol_test=",intersec_vol_test
		 print "accepted delta=",delta
		 sphere_radius_current=sphere_radius
		 print "current sphere_radius=",sphere_radius_current
		 intersec_vol_current=intersec_vol_test
		 print "current intersec_vol=",intersec_vol_test
		elif intersec_vol_test < intersec_vol_current and intersec_vol_test  > defvol or abs(intersec_vol_test-defvol) <= 10:
		 print "intersect_vol_test=",intersec_vol_test
		 print "accepted delta=",delta
		 sphere_radius_current=sphere_radius
		 print "current sphere_radius=",sphere_radius_current
		 intersec_vol_current=intersec_vol_test
		 print "current intersec_vol=",intersec_vol_test
		else:
		 print "bad delta,need to reduce delta"
		 delta=delta*0.75 #update delta, make it half the size of its precursor
		 print intersec_vol_test
	return sphere_radius_final
	


def main(args):

	if len(argv) != 7:
		print "usage: genDefect.py -l or -s inim angle defvol sphereim outim"
		print "       genDefect.py computes the coordinate of the com of a sphere located on the cortex of a kidney by sending a ray out from inside the kidney with a given angle(in degree) between the ray and the x-axis"
		sys.exit(1)
	raylen=70  #the length of the ray that is being sent out from the com of the cortex
	(LCortexIm, WCortexIm, theta, defvol, sphereim, outim)=ReadIm(args)

	#here you want to compute the com of one kidney, either left or right
	com=ndimage.measurements.center_of_mass(WCortexIm) #center of mass of the whole kidney
	lcom=ndimage.measurements.center_of_mass(LCortexIm) #center of mass of the left half kidney
	#x,y,z below are coordinates of the com of the left kidney, which server as the start point of the ray
	x=str(round(float(lcom[2]))) #must be a string 
	y=str(round(float(lcom[1]))) 
	z=str(round(float(lcom[0])))
	incrementx=raylen*np.cos(theta) #increment in x direction
	incrementy=raylen*np.sin(theta) #increment in y direction
	#incrementz=raylen*np.sin(theta) #increment in z direction
	xend=str(round(float(lcom[2]))+incrementx) #  end x coordinate 
	yend=str(round(float(lcom[1]))+incrementy) #  end y coordinate
	#zend=str(round(float(lcom[0]))+incrementz) #  end y coordinate
	#call improf
	if argv[1] == "-s" :
	 cmdimprof=['improf','-b',y,x,yend,xend,'-d',str(2),z,z,os.path.abspath(argv[2])] # everything inside must be a string, str(0) means in z direction
	elif argv[1] == "-l" :
	 cmdimprof=['improf','-b',x,y,xend,yend,'-d',str(0),z,z,os.path.abspath(argv[2])] # everything inside must be a string, str(0) means in z direction
	improfout=subprocess.check_output(cmdimprof) 
	newimprofout=improfout[improfout.index('\n')+1:] #skip reading the first row of improfout
	b=mat(newimprofout) #a 1d matrix of improf output
	u=b.reshape(b.shape[1]/2,2) # reshape b to get a N*2 matrix 

#	for i in range(u.shape[0]-1):
#	  if u[i,1]-u[i+1,1]==-1:
#		inbd=i+1 
#	  elif u[i,1]-u[i+1,1]==1:
#		outbd=i
	(inbd,outbd)=findIntersecs(u)
	xint=round(float(lcom[2]))
	yint=round(float(lcom[1]))
	zint=round(float(lcom[0])) 
	#print inbd,outbd
	corthickness=u[outbd,0]-u[inbd,0]+1 #+1 here in order to make the ellipsoid thiner
	print "cortex thickness in units of pixels=",corthickness
	#raydistance=(u[outbd,0]+u[inbd,0])/2
	raydistance=u[outbd,0]
	comspherex=round(xint+raydistance*np.cos(theta))
	comspherey=round(yint+raydistance*np.sin(theta))
	comsphere=[comspherex,comspherey,zint]
	Lcortex=LCortexIm.sum()
	#print "Left cortex total number of voxels=",Lcortex
	dims=map(int,WCortexIm.shape)
	pixsize=0.1
	activity=1
	actsphereim=sp.zeros(dims,sp.float32)
	#print WCortexIm.shape,dims
	##make a sphere
	sphere_radius=math.sqrt(3*2*defvol*pixsize**3/(4*math.pi*corthickness*pixsize))
	print "starting sphere_radius=",sphere_radius
	cz=(zint-0.5*dims[0]+0.5)*pixsize
	cy=(comspherey-0.5*dims[1]+0.5)*pixsize
	cx=(comspherex-0.5*dims[2]+0.5)*pixsize
	center=[cz,cy,cx]
	sphere=MakeEllipsoid(dims,pixsize,center,sphere_radius,corthickness)
	intersection=sphere*WCortexIm
	intersec_vol_current=intersection.sum()
	#determine stepsize delta
	intersec_vol=intersec_vol_current
	print intersec_vol
	sphere_radisu_pre=sphere_radius
	delta_accepted=0
	sphere_radius_current=sphere_radius
	if intersec_vol <= defvol :  # want to increase sphere volume
	 delta=0.02  #inital step size
	else:
	 delta=-0.02
	
#end of step size calculation
	(sphere_radius_final)=findOptSphere(defvol,delta,intersec_vol_current,sphere_radius_current,dims,pixsize,center,sphere_radius,corthickness,WCortexIm)
	center=[cz,cy,cx]
	sphere=MakeEllipsoid(dims,pixsize,center,sphere_radius_final,corthickness)
	intersection=sphere*WCortexIm
	intersec_vol=intersection.sum()	
	localdefect=WCortexIm*sphere*activity
	fim=WCortexIm-localdefect
	if argv[1] == "-s" :
	 ffim=fim.swapaxes(2,0)
	 swap_intersection=intersection.swapaxes(2,0)
	elif argv[1] == "-l" :
	 ffim=fim
	 swap_intersection=intersection
	ArrayToIm(ffim,outim)
	ArrayToIm(swap_intersection,sphereim)

main(sys.argv[1:])
