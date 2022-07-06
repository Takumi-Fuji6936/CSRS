import math
import pandas as pd
import numpy as np
import numpy.random as rd
import random
import os
import glob

def Ellipsoid(Slope,Optim,Forest_scale,new_path,N,Param_H,Param_DBH,Param_CR,Param_CL,Param_Int_x,Param_Int_y,Param_Int_z):

	files = glob.glob(new_path+"/*.txt")#os.listdir(new_path)  
	count = len(files)
	#print(count)
	#print(aaaaaaa)
	f = open(new_path+"/"+ str(count +1) +".txt",mode="w")
	#f = open(new_path + ".txt",mode="w")
	print("x y z Nx Ny Nz Tree_ID material",file=f)
	
	Stem = 0
	Canopy = 1
	Floor = 2
	
	Over = 5

	stem_it = 0.2

	Slope = math.radians(Slope)
	for j in range(N):
		Tree_ID = j

		
		Check = np.zeros(N-1)

		#Create Canopy stem
		#j番目のstemの高さ
		stem_h = Param_H[j] - Param_CL[j]

		theta_int = math.radians(10)
		theta_end = int(2*math.pi/theta_int)

		stem_r = (Param_DBH[j]/2)

		end_stem = int(stem_h / stem_it)
		for k in range(0,end_stem):

			for theta_stem in range(theta_end):
				
				x_stem = stem_r * math.cos(theta_stem*theta_int) + Param_Int_x[j]
				y_stem = stem_r * math.sin(theta_stem*theta_int) + Param_Int_y[j]
				z_stem = k*stem_it + Param_Int_z[j]

				Nx = 2 * math.cos(theta_stem*theta_int) / stem_r
				Ny = 2 * math.sin(theta_stem*theta_int) / stem_r

				DD = math.sqrt(Nx**2 + Ny**2)

				Nxx = round(Nx/DD,3)
				Nyy = round(Ny/DD,3)
				if x_stem>0 and x_stem<Forest_scale and y_stem>0 and y_stem<Forest_scale:
					

					print(round(x_stem,3),round(y_stem,3),round(z_stem,3),Nxx,Nyy,0,Tree_ID,Stem,file=f)


		#Create Canopy crown
		CR = Param_CR[j]
		CL = Param_CL[j]/2
		
		theta_range = int( (math.pi) / Optim[j] )+2
		fai_range = int( (2*math.pi) / Optim[j] )+2
		
		for theta_in in range(theta_range):

			for fai_in in range (fai_range):
	
				theta = theta_in * Optim[j]
			
				fai   = fai_in * Optim[j]

				x_ = CR * math.sin(theta) * math.cos(fai)
				y_ = CR * math.sin(theta) * math.sin(fai)
				z_ = CL * math.cos(theta) 

				# if y_>Thresh:
				# 	continue

				x = x_ + Param_Int_x[j]
				y = y_ + Param_Int_y[j]
				z = z_ + stem_h + CL + Param_Int_z[j]

				Nx = 2 * math.sin(theta) * math.cos(fai) /CR 
				Ny = 2 * math.sin(theta) * math.sin(fai) /CR 
				Nz = 2 * math.cos(theta) / CL

				DD = math.sqrt(Nx**2 + Ny**2 + Nz **2)

				Nxx = round(Nx/DD,3)
				Nyy = round(Ny/DD,3)
				Nzz = round(Nz/DD,3)
				
				ex_param_CR = np.delete(Param_CR,j)
				ex_param_CL = np.delete(Param_CL/2,j)
				ex_param_Int_x = np.delete(Param_Int_x,j)
				ex_param_Int_y = np.delete(Param_Int_y,j)
				ex_param_Int_z = np.delete(Param_H - Param_CL/2 + Param_Int_z,j)

				if CR > CL:
					radius = CR
				else:
					radius = CL

				#他の楕円体の内側に入っていないかチェック

				for t in range(len(ex_param_CR)):
					#他の楕円体のパラメータ
					CR_ex   = ex_param_CR[t]
					CL_ex   = ex_param_CL[t]
					#H_ex    = ex_param_H[t]

					Int_x_ex = ex_param_Int_x[t]
					Int_y_ex = ex_param_Int_y[t]
					Int_z_ex = ex_param_Int_z[t]

					if CR_ex > CL_ex:
						radius_ex = CR_ex
					else:
						radius_ex = CL_ex

					d = math.sqrt(( x - Int_x_ex )**2 + ( y - Int_y_ex )**2 )#+ ( z - Int_z_ex )**2)

					if abs(radius - radius_ex) < d and d < radius + radius_ex:

						Check[t] = ( x - Int_x_ex)**2 / CR_ex**2 + ( y - Int_y_ex)**2 / CR_ex**2 + ( z - Int_z_ex)**2 / CL_ex**2
					else:
						Check[t] = 2

				
				Check_point = len(np.where(Check<1)[0])
				
				if Check_point==0 and x>0 and x<Forest_scale and y>0 and y<Forest_scale:
					print(round(x,3),round(y,3),round(z,3),Nxx,Nyy,Nzz,Tree_ID,Canopy,file=f)
				else:
					pass
			

	#右下の楕円中心が(0,0,0)

	x_min = 0
	x_max = Forest_scale
	y_min = 0
	y_max = Forest_scale
	z_min = 0.0


	n = int(( x_max - x_min ) / 0.1 )
	Nx = 0
	Ny = 0
	Nz = 1
	#understory
	for i in range(n):

		for j in range(n):

			x = round(x_min + 0.1 * i,3)
			y = round(y_min + 0.1 * j,3)

			if x>0 and x<Forest_scale and y>0 and y<Forest_scale:
				print(x,y, y*math.sin(Slope),Nx,Ny,Nz,-1,Floor,file=f)


	f.close()
	return 0
		
		