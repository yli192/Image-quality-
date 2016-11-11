#! /mip/opt/bin/python

import numpy as np
import NumpyIm as npi
import sys
from sys import exit

if (len(sys.argv)<7):
   print "calcontrast.py defvol defloc phanbase csphere cortexphan recon2 "
   sys.exit()
defvol=sys.argv[1]
defloc=sys.argv[2]
phanbase=sys.argv[3]
inim1=sys.argv[4]
inim2=sys.argv[5]
inim3=sys.argv[6]

defvoi=npi.ArrayFromIm(inim1)
true_defvol=defvoi.sum()*8
#print true_defvol
bkgvoi=npi.ArrayFromIm(inim2)
#im=npi.ArrayFromIm('osads1.15F10.defup.v2741.10.im')
im=npi.ArrayFromIm(inim3)
#im1=npi.ArrayFromIm('/netscratch/garyli/im_quality/defect_simu/contrast/recons/recon2.defup.v300.00F10.im')
#multiply defvoi with im

defect=defvoi*im
#defect1=defvoi*im1
bkg=bkgvoi*im
#bkg1=bkgvoi*im1
S=defect.sum()/defvoi.sum()
#S1=defect1.sum()/defvoi.sum()
B=bkg.sum()/bkgvoi.sum()
#B1=bkg1.sum()/bkgvoi.sum()
contrast=abs(S-B)/B
#print 'signal=',S,'bkg=',B
#contrast1=abs(S1-B1)/B1
#print 'contrast=',contrast, 'processed im=',  inim3 #'contrast1=',contrast1
print contrast,true_defvol, defloc, inim3

