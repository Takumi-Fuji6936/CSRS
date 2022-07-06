import pandas as pd
import sys
import shutil
import numpy as np
#from tqdm import tqdm
#from time import sleep
import glob
import re
import os
from Compute_reflectance_tool import Voxelize
from Compute_reflectance_tool import SCS_main
from Compute_reflectance_tool import CS_main
from Compute_reflectance_tool import Ortho
from Compute_reflectance_tool import Reflectance
import CSRS_parameter
#import argparse

Forest_scale = CSRS_parameter.Forest_scale

Voxele_size  = CSRS_parameter.Voxel_size

CC = str(CSRS_parameter.CC).rjust(3,"0")

core_n = CSRS_parameter.core_n

shape = {0:'Ellipsoid',1:'Ellipsoid_half',2:'Ellipsoid_half_upside_down',3:'Cylinder'}

Param = CSRS_parameter.Dir + '/' + shape[int(CSRS_parameter.shape)] +'/CC_' +CC

n_dir = int(CSRS_parameter.n)

Sun_geometry = pd.read_csv( CSRS_parameter.Sun_geometry )

Lamda_file = pd.read_csv(CSRS_parameter.Lambda)
SRF_S      = pd.read_csv(CSRS_parameter.SRF)#pd.read_csv("Sensor_SRF/Sentinel_SRF/SRF/Spectral Responses (S2B)-表1.csv")
SRF_S      = SRF_S.fillna(-100)
SP_leaf    = pd.read_csv(CSRS_parameter.canopy,delim_whitespace=True,names=("wl","Ref"))#pd.read_csv('LEAF_2/vegetation.tree.prosopis.articulata.vswir.jpl142.jpl.asd.spectrum.txt',skiprows=20,delim_whitespace=True,names=("wl","Ref"))
SP_grass   = pd.read_csv(CSRS_parameter.floor,delim_whitespace=True,names=("wl","Ref"))#pd.read_csv('LEAF_2/vegetation.grass.avena.fatua.vswir.vh353.ucsb.asd.spectrum.txt',skiprows=20,delim_whitespace=True,names=("wl","Ref"))
IR         = CSRS_parameter.irradiance

vox_path = Param + "/2_Voxel"
SCS_path = Param + "/3_SCS"
cs_path  = Param + "/4_CS"
img_path = Param + "/5_image"
re_path  = Param + "/6_reflectance"
sp_path  = Param + "/7_split"


#Creat Voxel Dir---------------
if not os.path.exists( vox_path ):
	os.mkdir(vox_path)

else:
	pass
#--------------


#Creat SCS Dir---------------
if not os.path.exists( SCS_path ):
	os.mkdir(SCS_path)

else:
	pass
#---------------

#Creat CS Dir---------------
if not os.path.exists(cs_path):
		os.mkdir(cs_path)

else:
	shutil.rmtree(cs_path)
	os.mkdir(cs_path)
	pass

dir_list = np.arange(0,n_dir,1)
for d in dir_list:
	nnew_path = Param + "/4_CS/"+str(d)

	if not os.path.exists(nnew_path):
			os.mkdir(nnew_path)

	else:
		pass
#--------------


#Create ortho img dir -------------
if not os.path.exists(img_path):
	os.mkdir(img_path)

else:
	shutil.rmtree(img_path)
	os.mkdir(img_path)
	pass

for d in dir_list:
	nnew_path = img_path + "/" +str(d)
	
	if not os.path.exists(nnew_path):
		os.mkdir(nnew_path)

	else:
		shutil.rmtree(nnew_path)
		os.mkdir(nnew_path)
		pass

#--------------


#Create reflecatnce dir -------------
if not os.path.exists(re_path):
	os.mkdir(re_path)

else:
	shutil.rmtree(re_path)
	os.mkdir(re_path)
	pass


for d in dir_list:
	nnew_path = re_path + "/" +str(d)
	
	if not os.path.exists(nnew_path):
		os.mkdir(nnew_path)

	else:
		shutil.rmtree(nnew_path)
		os.mkdir(nnew_path)
		pass

#--------------


point_files = glob.glob( Param +"/1_PointCloud/*.txt")
Voxelize.Voxelize(point_files,vox_path,Voxele_size)

vox_files = glob.glob(Param +"/2_Voxel/*.txt")
SCS_main.SCS_main( vox_files,SCS_path,Forest_scale,Voxele_size,core_n)

scs_files = np.sort(glob.glob(Param+"/3_SCS/*.txt"))
CS_main.CS_main(scs_files,cs_path,Voxele_size,Sun_geometry)

Ortho.Ortho(cs_path,img_path,n_dir,Voxele_size,Sun_geometry)

Reflectance.Reflectance(img_path,re_path,n_dir,Lamda_file,SRF_S,SP_leaf,SP_grass,Sun_geometry,IR)
