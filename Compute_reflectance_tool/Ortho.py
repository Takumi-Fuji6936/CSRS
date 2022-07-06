import pandas as pd
import sys
import numpy as np
from tqdm import tqdm
from osgeo import gdal
from osgeo import gdal_array
import glob
import re
import os
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

def Ortho(nnew_path,new_path,N_dir,VS,Sentinel_Sun_list):
	
	zeni_list = Sentinel_Sun_list["SZA"]
	Azi_list  = Sentinel_Sun_list["SAA"]
	Date_list = Sentinel_Sun_list["Date"]
	Year_list = Sentinel_Sun_list["Year"]


	for i_sh in range(N_dir):
		files = np.sort(glob.glob(nnew_path+"/"+str(i_sh)+"/*.txt"))
		print(files)

		fff = files[0]

		
		ff = re.split('[_/.]',fff)
		ff_num = ff[-10] 
	
		Merge_df = pd.DataFrame()

		for Zenith,Azimuth,Date,Year in zip(zeni_list,Azi_list,Date_list,Year_list):

			Date = str(Date).zfill(4)
			
			Zenith  = str(round(Zenith,3))
			Azimuth = str(round(Azimuth,3))
			Year    = str(round(Year,3))

			dir_shadow = nnew_path+"/"+str(i_sh)
			f = nnew_path+"/"+str(i_sh)+"/"+ ff_num + "_vox_SCS_CS"+Year +"_"+ Date +"_"+ Zenith +"_"+ Azimuth +".txt"
			#print(f)
			data = pd.read_csv(f,delim_whitespace=True)
			#print(data)
			Merge_df["CS_"+Zenith] = data["CS"]

			del data["CS"]
			data = pd.concat([data,Merge_df],axis=1)

			data = data[data["SCS"]>-0.0000000001]
			data = data.sort_values(["x","y","z"])
		
		
			X = np.array(data["x"]) 
			Y = np.array(data["y"]) 
			Z = np.array(data["z"])
			SCS = np.array(data["SCS"])
			M = np.array(data["Material"])


			SZA = data.values[:,-1]
			
			Nx = np.array(data["Nx"])
			Ny = np.array(data["Ny"])
			Nz = np.array(data["Nz"])

			XX = np.array(data["xx"])
			YY = np.array(data["yy"])
			ZZ = np.array(data["zz"])

			data_col = data.columns.values


			Num_Vox = 0


			iim_name = str(i_sh) + "_vox_CS_"+ Year + "_" + Date +"_"+ Zenith +"_"+ Azimuth

			f_name = new_path+"/"+ str(i_sh) +"/" +iim_name+"_ortho.txt"	

			f = open(f_name,mode="w")
			
			print ('x','y','z','nx','ny','nz','SCS',
				data_col[-1],
				'M','Num_Vox',file=f)

			for i in tqdm(range(0,len(Z)-1)):

				x0=X[i]
				x1=X[i+1]

				y0=Y[i]
				y1=Y[i+1]

				z0=Z[i]
				z1=Z[i+1]
	 
				nx0 = Nx[i]
				ny0 = Ny[i]
				nz0 = Nz[i]
				
				av_x = XX[i]
				av_y = YY[i]
				av_z = ZZ[i]
				svf  = SCS[i]
				m  = M[i]
				

				sza = SZA[i]
				
				if (x0 == x1 and y0 == y1):
					Num_Vox+=1
					#continue

				else:

					print (x0,y0,z0,nx0,ny0,nz0,svf,
						sza,m,Num_Vox,file=f)

					Num_Vox=0
			f.close()
		

			data=pd.read_csv(f_name,delim_whitespace=True)

			Vox_Sizse = VS

			X   = np.array(data["x"])
			Y   = np.array(data["y"])
			Z   = np.array(data["z"])
			NX  = np.array(data["nx"])
			NY  = np.array(data["ny"])
			NZ  = np.array(data["nz"])

			SCS = np.array(data["SCS"])

			M   = np.array(data["M"])
			

			CS  = data.values[:,-3]
				
			COL = data.columns.values
			
			Name_01 = COL[-3]
			
			N_v = np.array(data["Num_Vox"])

			x_min = np.min(X)
			y_min = np.min(Y)
			y_max = np.max(Y) 

			z_min = np.min(Z)

			X_num = ( data["x"] -  x_min ) / Vox_Sizse
			Y_num = ( data["y"] -  y_min ) / Vox_Sizse
			X_num = X_num.map(lambda x: float(Decimal(str(x))
														.quantize(Decimal("0.001"),rounding=ROUND_HALF_UP)))

			Y_num = Y_num.map(lambda x: float(Decimal(str(x))
														.quantize(Decimal("0.001"),rounding=ROUND_HALF_UP)))



			I_num = np.floor(X_num).astype(np.int)
			J_num = np.floor( np.max(Y_num) - Y_num).astype(np.int)
			
			x_pixels = int(np.max(I_num) + 1)
			y_pixels = int(np.max(J_num) + 1)

			Rayer = 8

			image = np.zeros((Rayer,y_pixels,x_pixels),np.float32)

			for i in range(len(X)):
				image[0][J_num[i]][I_num[i]] = Z[i]
				image[1][J_num[i]][I_num[i]] = NX[i]
				image[2][J_num[i]][I_num[i]] = NY[i]
				image[3][J_num[i]][I_num[i]] = NZ[i]
				image[4][J_num[i]][I_num[i]] = SCS[i]
				image[5][J_num[i]][I_num[i]] = CS[i]/4
				image[6][J_num[i]][I_num[i]] = M[i]
				image[7][J_num[i]][I_num[i]] = N_v[i]
		
			RRR = pd.DataFrame()

			RRR['Band'] = np.arange(Rayer)
			RRR['Name'] = np.array(('Z','NX','NY','NZ','SCS','CS','M','N_v'))

			RRR.to_csv(new_path+"/band_name.txt",index=False,sep=" ")


			driver = gdal.GetDriverByName('GTiff')
			dataset = driver.Create(
				new_path+"/"+str(i_sh)+"/"+ iim_name +"_ortho.tif",
			    x_pixels,
				y_pixels,
				Rayer,
				gdal.GDT_Float64, )

			dataset.SetGeoTransform((
			        x_min,  
			        Vox_Sizse, 
			        0,                     
			        y_max,   
			        0,                   
			        -Vox_Sizse))  
			
			for i in range(Rayer):

				dataset.GetRasterBand(i+1).WriteArray(image[i,:,:])
			
			dataset.FlushCache()  

			dataset = None

			