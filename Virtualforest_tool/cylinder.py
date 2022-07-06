import math
import pandas as pd
import numpy as np
import numpy.random as rd
import random
import os
import glob

def Cylinder(Slope,Optim,Optim_stem,Forest_scale,new_path,N,Param_H,Param_DBH,Param_CR,Param_CL,Param_Int_x,Param_Int_y,Param_Int_z):

	files = glob.glob(new_path+"/*.txt")#os.listdir(new_path)  
	count = len(files)
	Param_stem_h = Param_H - Param_CL
	
	f = open(new_path+"/"+ str(count +1) +".txt",mode="w")

	print("x y z Nx Ny Nz Tree_ID material",file=f)
	
	#Material_ID
	Stem = 0
	Canopy = 1
	Floor = 2
	
	for j in range(N):
		Tree_ID = j


		Check = np.zeros(N-1)
		Check_iner = np.zeros(N-1)
		Check_lower = np.zeros(N-1)


		#Create Canopy stem---------------------
		
		#j番目のstem height
		stem_h = Param_stem_h[j]
		stem_r_ori = (Param_DBH[j]/2)

		#print(j,round(Param_Int_x[j],3),round(Param_Int_y[j],3))

		#半径がDBHの円を描く時の角度の間隔(radian)
		theta_int_ori = Optim_stem[j]
		theta_end = int(2*math.pi/theta_int_ori)

		stem_it = 0.2

		end_stem = int(stem_h / stem_it)

		for k in range(0,end_stem):

			for theta_stem in range(theta_end):
				
				x_stem = stem_r_ori * math.cos(theta_stem*theta_int_ori) + Param_Int_x[j]
				y_stem = stem_r_ori * math.sin(theta_stem*theta_int_ori) + Param_Int_y[j]
				z_stem = k * stem_it + Param_Int_z[j]

				Nx = 2 * math.cos(theta_stem*theta_int_ori) / stem_r_ori
				Ny = 2 * math.sin(theta_stem*theta_int_ori) / stem_r_ori

				DD = math.sqrt(Nx**2 + Ny**2)

				Nxx = round(Nx/DD,3)
				Nyy = round(Ny/DD,3)
				if x_stem>0 and x_stem<Forest_scale and y_stem>0 and y_stem<Forest_scale:
					

					print(round(x_stem,3),round(y_stem,3),round(z_stem,3),Nxx,Nyy,0,Tree_ID,Stem,file=f)
		#------------------------


		#Create Canopy crown---------------------

		#半径がCRの円を描く時の角度の間隔(radian)
		theta_int_ori = Optim_stem[j] * 1/(Param_CR[j]   / stem_r_ori)
		theta_end = int(2*math.pi/theta_int_ori)+1
		
		end_crown = int(Param_CL[j]/stem_it)
		#print(theta_int_ori,Optim_stem[j],theta_end)
		for k in range(0,end_crown):

			for theta_stem in range(theta_end):
				
				x = Param_CR[j] * math.cos(theta_stem*theta_int_ori) + Param_Int_x[j]
				y = Param_CR[j] * math.sin(theta_stem*theta_int_ori) + Param_Int_y[j]
				z = k*stem_it + stem_h + Param_Int_z[j]

				Nx = 2 * math.cos(theta_stem*theta_int_ori) / Param_CR[j]
				Ny = 2 * math.sin(theta_stem*theta_int_ori) / Param_CR[j]

				DD = math.sqrt(Nx**2 + Ny**2)

				Nxx = round(Nx/DD,3)
				Nyy = round(Ny/DD,3)



				ex_param_CL = np.delete(Param_CL,j)
				ex_param_CR = np.delete(Param_CR,j)
				ex_param_Int_x = np.delete(Param_Int_x,j)
				ex_param_Int_y = np.delete(Param_Int_y,j)
				ex_param_stem_h = np.delete(Param_stem_h,j)


				#生成したxyzが他の円の外側にあればよい
				for t in range(len(ex_param_CR)):
					r_ex   = ex_param_CR[t]
					Int_x_ex = ex_param_Int_x[t]
					Int_y_ex = ex_param_Int_y[t]
					stem_h_ex = ex_param_stem_h[t]

					AA = (( x - Int_x_ex)**2 / r_ex**2 ) + (( y - Int_y_ex)**2 / r_ex**2 )

					#t番目の三角錐の内側かチェック,プラスなら外側、マイナスなら内側
					Check_iner[t] = AA - 1

					#t番目の三角錐の下かチェック,プラスなら上、マイナスなら下
					Check_lower[t] = z - (stem_h_ex + ex_param_CL[t] )

				Check_iner_len = np.where(Check_iner<0,0,1)

				Check_lower_len = np.where(Check_lower<0,0,1)

				Check = Check_iner_len + Check_lower_len
 
				Check_point = len(np.where(Check==0)[0])

				if Check_point == 0 and x>0 and x<Forest_scale and y>0 and y<Forest_scale:
					

					print(round(x,3),round(y,3),round(z,3),Nxx,Nyy,0,Tree_ID,Canopy,file=f)


		#------------------------

		r_num  = int(Param_CR[j] / stem_it) +1

		for r_it in range(1,r_num):
			stem_r = r_it * stem_it

			# if stem_r > Param_CR[j]:
			# 	print("aaaaaa")
			# 	continue

			#半径がstem_rの時の点の間隔
			theta_int = Optim_stem[j] *  1/(stem_r / stem_r_ori )

			theta_end = int(2*math.pi/theta_int) +1

			for theta_stem in range(theta_end):

				x_stem = stem_r * math.cos(theta_stem*theta_int) + Param_Int_x[j]
				y_stem = stem_r * math.sin(theta_stem*theta_int) + Param_Int_y[j]
				z_stem = Param_CL[j] + stem_h + Param_Int_z[j]

				Nxx = 0#round(Nx/DD,3)
				Nyy = 0#round(Ny/DD,3)
				if x_stem>0 and x_stem<Forest_scale and y_stem>0 and y_stem<Forest_scale:
					

					print(round(x_stem,3),round(y_stem,3),round(z_stem,3),Nxx,Nyy,1,Tree_ID,Canopy,file=f)	
		

	#understory
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
	
	for i in range(n):

		for j in range(n):

			x = round(x_min + 0.1 * i,3)
			y = round(y_min + 0.1 * j,3)

			if x>0 and x<Forest_scale and y>0 and y<Forest_scale:
				print(x,y,y*math.sin(Slope),Nx,Ny,Nz,-1,Floor,file=f)


	f.close()
	return 0