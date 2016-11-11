#! /mip/opt/bin/python

import sys, os, subprocess
import numpy as np
from sys import exit, argv
from NumpyIm import ArrayFromIm, ArrayToIm

if len(argv) != 10:
        print "usage: sprj.py phanbase act_toi fraction_wk fraction_liv fraction_spl cor-to-med+pel_ratio Acqtime defloc outprjim"
        sys.exit(1)
actmapdir='/netscratch/garyli/im_quality/squared_actmap/'
prjsdir='/netscratch/garyli/im_quality/raw_projection/'
#sprjsdir='/netscratch/garyli/im_quality/scaled_projection/'
defactmapdir='/netscratch/garyli/im_quality/defect_actmaps/'
defprjdir='/netscratch/garyli/im_quality/def_raw_projs/'
cp=30 #use a fixed defect contrast percentile;hard coded below
phanbase=argv[1]
age=phanbase[:2]
if phanbase[3]=='R':
   weightpercentile=50
else:
   weightpercentile=phanbase[3:5]
gender=phanbase[2]
Atoi=float(argv[2]) # in units of mCi
kwk=float(argv[3])
cratio=float(argv[6]) # cortex-to-medulla+pelvis concentration ratio
Acqtime=float(argv[7])
kliv=float(argv[4])
kspl=float(argv[5])
defloc_num=argv[8]
outfname=argv[9]
#defsize="****"
#4 deflocs : 1=defect free,2=up,3=lp,4=lat
if defloc_num == "1" :
 CorActIm=[actmapdir,'c/',age,'/',weightpercentile,'/',phanbase,'.x.sq.c.im']
 CorPrjIm=[prjsdir,'c/',age,'/',weightpercentile,'/',phanbase,'.proj.c.im']
elif defloc_num =="2" :
 defloc="up"
 if age == '01' or age == '05' or age == '00':
  CorActIm=[defactmapdir,'unisex/',age,'/','def.',defloc,'.',phanbase,'.cp30.im'] #here use 1 defect actmap to keep act in cor low
  CorPrjIm=[defprjdir,'unisex/',age,'/',phanbase,'.',defloc,'.defprj.c.cp30.im']
  #OutPath=[sprjdir,'unisex/',age,'/',outfname]
 else:
  if gender=='M':
        CorActIm=[defactmapdir,'male/',age,'/','def.',defloc,'.',phanbase,'.cp30.im']
        CorPrjIm=[defprjdir,'male/',age,'/',phanbase,'.',defloc,'.defprj.c.cp30.im']
        #OutPath=[sprjdir,'male/',age,'/',outfname]
  else:
        CorActIm=[defactmapdir,'female/',age,'/','def.',defloc,'.',phanbase,'.cp30.im']
        CorPrjIm=[defprjdir,'female/',age,'/',phanbase,'.',defloc,'.defprj.c.cp30.im']
        #OutPath=[sprjdir,'female/',age,'/',outfname]
elif defloc_num =="3" :
 defloc="lp"
 if age == '01' or age == '05' or age == '00':
  CorActIm=[defactmapdir,'unisex/',age,'/','def.',defloc,'.',phanbase,'.cp30.im'] #here use 1 defect actmap to keep act in cor low
  CorPrjIm=[defprjdir,'unisex/',age,'/',phanbase,'.',defloc,'.defprj.c.cp30.im']
  #OutPath=[sprjdir,'unisex/',age,'/',outfname]
 else:
  if gender=='M':
        CorActIm=[defactmapdir,'male/',age,'/','def.',defloc,'.',phanbase,'.cp30.im']
        CorPrjIm=[defprjdir,'male/',age,'/',phanbase,'.',defloc,'.defprj.c.cp30.im']
        #OutPath=[sprjdir,'male/',age,'/',outfname]
  else:
        CorActIm=[defactmapdir,'female/',age,'/','def.',defloc,'.',phanbase,'.cp30.im']
        CorPrjIm=[defprjdir,'female/',age,'/',phanbase,'.',defloc,'.defprj.c.cp30.im']
        #OutPath=[sprjdir,'female/',age,'/',outfname]
elif defloc_num == "4" :
 defloc="lat"
 if age == '01' or age == '05' or age == '00':
  CorActIm=[defactmapdir,'unisex/',age,'/','def.',defloc,'.',phanbase,'.cp30.im'] #here use 1 defect actmap to keep act in cor low
  CorPrjIm=[defprjdir,'unisex/',age,'/',phanbase,'.',defloc,'.defprj.c.cp30.im']
  #OutPath=[sprjdir,'unisex/',age,'/',outfname]
 else:
  if gender=='M':
        CorActIm=[defactmapdir,'male/',age,'/','def.',defloc,'.',phanbase,'.cp30.im']
        CorPrjIm=[defprjdir,'male/',age,'/',phanbase,'.',defloc,'.defprj.c.cp30.im']
        #OutPath=[sprjdir,'male/',age,'/',outfname]
  else:
        CorActIm=[defactmapdir,'female/',age,'/','def.',defloc,'.',phanbase,'.cp30.im']
        CorPrjIm=[defprjdir,'female/',age,'/',phanbase,'.',defloc,'.defprj.c.cp30.im']
        #OutPath=[sprjdir,'female/',age,'/',outfname]
#CorActIm=[actmapdir,'c/',age,'/',weightpercentile,'/',phanbase,'.x.sq.c.im']
MedActIm=[actmapdir,'m/',age,'/',weightpercentile,'/',phanbase,'.x.sq.m.im']
PelActIm=[actmapdir,'p/',age,'/',weightpercentile,'/',phanbase,'.x.sq.p.im']
LivActIm=[actmapdir,'l/',age,'/',weightpercentile,'/',phanbase,'.x.sq.l.im']
SplActIm=[actmapdir,'s/',age,'/',weightpercentile,'/',phanbase,'.x.sq.s.im']
BkgActIm=[actmapdir,'bg/',age,'/',weightpercentile,'/',phanbase,'.x.sq.bg.im']
#CorPrjIm=[prjsdir,'c/',age,'/',weightpercentile,'/',phanbase,'.proj.c.im']
MedPrjIm=[prjsdir,'m/',age,'/',weightpercentile,'/',phanbase,'.proj.m.im']
PelPrjIm=[prjsdir,'p/',age,'/',weightpercentile,'/',phanbase,'.proj.p.im']
LivPrjIm=[prjsdir,'l/',age,'/',weightpercentile,'/',phanbase,'.proj.l.im']
SplPrjIm=[prjsdir,'s/',age,'/',weightpercentile,'/',phanbase,'.proj.s.im']
BkgPrjIm=[prjsdir,'bg/',age,'/',weightpercentile,'/',phanbase,'.proj.bg.im']

im=["".join([str(i) for i in CorActIm]), "".join([str(i) for i in MedActIm]), "".join([str(i) for i in PelActIm]), "".join([str(i) for i in LivActIm]), "".join([str(i) for i in SplActIm]), "".join([str(i) for i in BkgActIm]), "".join([str(i) for i in CorPrjIm]),"".join([str(i) for i in MedPrjIm]),"".join([str(i) for i in PelPrjIm]), "".join([str(i) for i in LivPrjIm]), "".join([str(i) for i in SplPrjIm]), "".join([str(i) for i in BkgPrjIm])]
inim=[ArrayFromIm(i) for i in im[0:12]]
#voxelized volume of body from UF data, cm^3
bodyvolume={'00M10':3296.047,'00M50':3374.781,'00M90':3421.933,'00F10':3293.573,'00F50':3371.772,'00F90':3420.073,'01M10':10127.18,'01M50':9830.294,'01M90':10164.51,'01F10':10119.42,'01F50':9829.417,'01F90':10140.83,'05M10':19142.31,'05M50':18937.15,'05M90':18882.49,'05F10':19193.75,'05F50':18926.71,'05F90':18923.6,'10M10':28770,'10M50':32795.6,'10M90':29061.36,'10F10':33987.43,'10F50':32786.39,'10F90':33541.98,'15M10':53543.69,'15M50':57431.04,'15M90':53282.64,'15F10':49217.4,'15F50':53905.92,'15F90':48921.77}
bodyvolumekey=[age,gender,weightpercentile]
m="".join([str(v) for v in bodyvolumekey]) #convert a list of ints to a string
vb=bodyvolume[m]
VoxelVol=0.001 #cm^3
#calculate the number of voxels in each organ/inim
Nc=np.sum(inim[0])
Nm=np.sum(inim[1])
Np=np.sum(inim[2])
Nl=np.sum(inim[3])
Ns=np.sum(inim[4])
Nbg=np.sum(inim[5])
vorgan=Nc*VoxelVol+Nm*VoxelVol+Np*VoxelVol+Ns*VoxelVol+Nl*VoxelVol
vbr=vb-vorgan #cm^3
#calculate activity per voxel for each organ
peluptake=0.12 #fixed based on segmentation results
meduptake=0.12
Al=Atoi*kliv
As=Atoi*kspl
Abg=Atoi*(1-kliv-kspl-kwk)
Awk=Atoi*kwk
Alpv=Al/Nl
Aspv=As/Ns
Abgpv=Atoi*(1-kliv-kspl-kwk)/vbr*VoxelVol
Ampv=Awk/(((Np*Nc*cratio+Nc*cratio*Nm)/(Np+Nm))+Nm+Np)
Appv=Ampv*peluptake/meduptake
Acpv=(Awk-(Nm*Ampv+Np*Appv))/Nc
#count in the acquistion time and convert units to counts
Clpv=Alpv*Acqtime*100000/60
Cspv=Aspv*Acqtime*100000/60
Cbgpv=Abgpv*Acqtime*100000/60
Ccpv=Acpv*Acqtime*100000/60
Cmpv=Ampv*Acqtime*100000/60
Cppv=Appv*Acqtime*100000/60
Cbgpv=Abgpv*Acqtime*100000/60
ratio=Ccpv/((Cmpv*Nm+Cppv*Np)/(Nm+Np))
print 'phantom base',phanbase
print 'k_wk=',kwk,'k_liv=',kliv,'k_spl=',kspl,'k_bkg=',(1-kliv-kspl-kwk)
print 'cortex/medulla+pelvis activity concentration ratio=',ratio
print 'corvox#=',Nc,'medvox#=', Nm,'pelvox#=',Np,'livvox#=', Nl,'splvox#=',Ns, 'bkgvox#=', Nbg
print 'counts per voxel in cortex, medulla, pelvis, liver, spleen, bkg=',Ccpv,Cmpv,Cppv,Clpv,Cspv, Cbgpv
print 'output scaled image name=',outfname
outim=inim[6]*Ccpv+inim[7]*Cmpv+inim[8]*Cppv+inim[9]*Clpv+inim[10]*Cspv+inim[11]*Cbgpv
ArrayToIm(outim,outfname)
