from Virtualforest_tool import ellipsoid
from Virtualforest_tool import ellipsoid_half
from Virtualforest_tool import ellipsoid_half_upside_down
from Virtualforest_tool import Optimise_fai_theta
from Virtualforest_tool import cylinder
from Virtualforest_tool import tree_location
import CSRS_parameter
import os
import shutil
import numpy as np
import time
import argparse

#Create working directory
Foldar = CSRS_parameter.Dir
if not os.path.exists( Foldar ):
	os.mkdir(Foldar)


Forest_scale = CSRS_parameter.Forest_scale

Voxel_size = CSRS_parameter.Voxel_size

CC = CSRS_parameter.CC 

TH_ave = CSRS_parameter.th_ave

TH_std = CSRS_parameter.th_std

CR_ave = CSRS_parameter.cr_ave 

CR_std = CSRS_parameter.cr_std 

DBH = CSRS_parameter.dbh


mydict = {0:"Ellipsoid",1:"Ellipsoid_half",2:"Ellipsoid_half_upside_down",
 			3:"Cylinder"}

Num = CSRS_parameter.n

Slo = CSRS_parameter.slope 

Asym = 1.0

for iii in range(Num):

	start = time.time()

	Cover,RRR,CCC,Param_Int_x,Param_Int_y,Param_Int_z,Param_CR,Param_H,Param_DBH,Param_CLL = tree_location.tree_location(Forest_scale,CC,TH_ave,TH_std,Slo,Asym,CR_ave,CR_std,DBH)
	
	try:
		N = len(Param_Int_y)
		print(iii)

	except :
		print('Number of tree is 1.')
		print('At least two trees are required to create virtual forest.')
		print('Please try again or change the parameters.')
		sys.exit()

	#elapsed_time = time.time() - start

	#print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

	for shape in mydict:
					
		#print(iii,mydict[shape],"CCC",Cover ,file=f)

		print(mydict[shape])	

					
		if mydict[shape] == "Ellipsoid_half" or  mydict[shape] == "Ellipsoid_half_upside_down":
			Param_CL = Param_CLL*2
		else:
			Param_CL = Param_CLL

		Param_CRCL = np.zeros(N)
					
		for i in range(N):
			CR = Param_CR
			CL = Param_CL

			if CR[i] > CL[i]/2 :
				Large = CR[i]
			else:
				Large = CL[i]/2

			Param_CRCL[i] = Large


		Optim = Optimise_fai_theta.fai_theta(Voxel_size,Param_CRCL,3000)

		Optim_stem = Optimise_fai_theta.fai_theta(Voxel_size,Param_DBH/2,90000)
		


		
		Shape_path = Foldar +"/"+mydict[shape]
		if not os.path.exists( Shape_path ):
			os.mkdir(Shape_path)

		else:
			pass


		Param_CC = str(int(CC))
		CC_path = Shape_path + "/CC_"+Param_CC.rjust(3,"0")
		if not os.path.exists( CC_path ):
		 	os.mkdir(CC_path)

		else:
			pass



		new_path = CC_path + "/1_PointCloud"
		if not os.path.exists( new_path ):
			os.mkdir(new_path)

		else:
			pass

		if iii == 0:
			shutil.rmtree(CC_path + "/1_PointCloud"+"/")
		
		new_path = CC_path + "/1_PointCloud"
		if not os.path.exists( new_path ):
			os.mkdir(new_path)

		else:
			pass
		

		print(new_path,mydict[shape])
		print(N)

		if   mydict[shape] == "Ellipsoid":
			ellipsoid.Ellipsoid(Slo,Optim,Forest_scale,new_path,N,Param_H,Param_DBH,Param_CR,Param_CL,Param_Int_x,Param_Int_y,Param_Int_z)

		elif mydict[shape] == "Ellipsoid_half":
			ellipsoid_half.Ellipsoid_half(Slo,Optim,Optim_stem,Forest_scale,new_path,N,Param_H,Param_DBH,Param_CR,Param_CL,Param_Int_x,Param_Int_y,Param_Int_z)
		
		elif mydict[shape] == "Ellipsoid_half_upside_down":
			ellipsoid_half_upside_down.Ellipsoid_half_upside_down(Slo,Optim,Optim_stem,Forest_scale,new_path,N,Param_H,Param_DBH,Param_CR,Param_CL,Param_Int_x,Param_Int_y,Param_Int_z)
		
		elif mydict[shape] == "Cylinder":
			cylinder.Cylinder(Slo,Optim,Optim_stem,Forest_scale,new_path,N,Param_H,Param_DBH,Param_CR,Param_CL,Param_Int_x,Param_Int_y,Param_Int_z)
