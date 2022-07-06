import math
import numpy as np
import pandas as pd
import sys
import os
from time import sleep
from tqdm import tqdm
import time
from Compute_reflectance_tool import CS_compute
from osgeo import gdal
import glob
import re
	
def CS_main(files,new_path,VS,Sentinel_Sun_list):

	ff = 0
	for f in files:
		f_name = re.split('[/.]',f)[-2]
		print(f_name)
		df1 = pd.read_csv(f,delim_whitespace=True)
		ID_ = df1["ID"][(df1["SCS"]>=0)&(df1["Material"]==1)]

		VOXEL_SIZE = VS
		
		X = np.array(df1["x"]).astype(np.float32)
		Y = np.array(df1["y"]).astype(np.float32)
		Z = np.array(df1["z"]).astype(np.float32)

		zeni_list = Sentinel_Sun_list["SZA"]
		Azi_list  = Sentinel_Sun_list["SAA"]
		Date_list = Sentinel_Sun_list["Date"]
		Year_list = Sentinel_Sun_list["Year"]
		
		for Zenith,Azimuth,Date,Year in zip(zeni_list,Azi_list,Date_list,Year_list):
			

			print(f,Zenith)
			Date    = str(Date).zfill(4)
			
			Zenith  = round(Zenith,3)
			Azimuth = round(Azimuth,3)
		
			sun_alt,sun_az = 90- Zenith,Azimuth


			S_AZIMUTH   = math.radians(90.0-sun_az)
			S_ELEVATION = math.radians(-sun_alt)

			#Vector to Sun
			a = math.cos(S_ELEVATION) * math.cos(S_AZIMUTH) 
			b = math.cos(S_ELEVATION) * math.sin(S_AZIMUTH) 
			c = - math.sin(S_ELEVATION)
			#print (a,b,c)

			N = int(len(df1.index))

			t = time.time()
			
			DD_1 = np.zeros(N,dtype=np.uint16) 
		
			AA = CS_compute.pairwise_numba(X,Y,Z,a,b,c,DD_1,N,VOXEL_SIZE)

			df1["CS"] = AA

			df1.to_csv(new_path+"/"+str(ff)+"/"+ f_name+"_CS"+str(Year)+"_"+str(Date)+"_"+str(Zenith)+"_"+str(Azimuth)+".txt",index=False,sep=" ")
			
		ff+=1