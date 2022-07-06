import numpy as np
from osgeo import gdal
import math
import sys
import glob
import re
import pandas as pd
from osgeo import ogr, osr


def Reflectance(nnew_path,re_path,N_dir,Lamda,SRF_S,SP_leaf,SP_grass,Sun_geometry,IR):

	for i_n in range(N_dir):
		files = np.sort(glob.glob(nnew_path+"/"+str(i_n)+"/*.tif"))

		Leaf_ref = SP_leaf
		Grass_ref = SP_grass

		for f in files:

			dat = gdal.Open(f, gdal.GA_ReadOnly)

			print(f)
			
			Y_it = re.split('[_/]',f)[-5]
			M_it = re.split('[_/]',f)[-4][0:2]
			D_it = re.split('[_/]',f)[-4][2:4]
			SZA_it = re.split('[_/]',f)[-3]
			SAA_it = re.split('[_/]',f)[-2]

			print(Y_it,M_it,D_it)

			geotransform = dat.GetGeoTransform()

			DSM = np.array(dat.GetRasterBand(1).ReadAsArray()).astype(np.float32)
			Nx = np.array(dat.GetRasterBand(2).ReadAsArray()).astype(np.float32)
			Ny = np.array(dat.GetRasterBand(3).ReadAsArray()).astype(np.float32)
			Nz = np.array(dat.GetRasterBand(4).ReadAsArray()).astype(np.float32)
			SCS = np.array(dat.GetRasterBand(5).ReadAsArray()).astype(np.float32)
			CS = np.array(dat.GetRasterBand(6).ReadAsArray()).astype(np.float32)
			M = np.array(dat.GetRasterBand(7).ReadAsArray()).astype(np.float32)
			N_V = np.array(dat.GetRasterBand(8).ReadAsArray()).astype(np.float32)
			
			Sat_x_pixels = dat.RasterXSize
			Sat_y_pixels = dat.RasterYSize

			Sat_PIXEL_SIZE_x = geotransform[1]
			Sat_PIXEL_SIZE_y = geotransform[5]

			Sat_x_min = geotransform[0]
			Sat_y_max = geotransform[3]
			
			#Band
			N=2
			for Band in range(len(Lamda)):

				#Wavelength
				B = str(Lamda["Band"][Band])

				Lamda_1 =  Lamda["lamda1"][Band]*10**(-3)
				Lamda_2 =  Lamda["lamda2"][Band]*10**(-3)
				Lamda_1 = round(Lamda_1,3)
				Lamda_2 = round(Lamda_2,3)
				#print(B)
				#print(Lamda_1,Lamda_2)
				
				print(B)
				
				if B!='B11' and B!='B12':

					#band_dict = {'B02':'B2','B03':'B3','B04':'B4'}
					
					temp_SRF = SRF_S.iloc[:,N][(SRF_S["SR_WL"]>=Lamda_1*10**3)&(SRF_S["SR_WL"]<=Lamda_2*10**3)]
					SRF_value = np.array(temp_SRF)
					SRF_sum = SRF_value.sum()

					temp_leaf = Leaf_ref["Ref"][(Leaf_ref["wl"]>=Lamda_1)&(Leaf_ref["wl"]<=Lamda_2)]
					leaf_value = np.array(temp_leaf)/100

					temp_grass = Grass_ref["Ref"][(Grass_ref["wl"]>=Lamda_1)&(Grass_ref["wl"]<=Lamda_2)]
					grass_value = np.array(temp_grass)/100

					N+=1
					
					#num_band = 5
					Out = np.zeros((Sat_x_pixels,Sat_y_pixels))
		
					ext_df = pd.read_csv(IR+"/"+B+"/ext/"+str(Y_it)+'_'+M_it+'_'+D_it+".ext.txt",delim_whitespace=True)
				
					b = np.array(ext_df["Difuse_horizn_irradiance"])*10**(3)#.mean()
					c = np.array(ext_df["Direct_horizn_irradiance"])*10**(3)#.mean()
					d = np.array(ext_df["Extraterrestrial_spectrm"])*10**(3)#.mean()

					#print(len(SRF_value),len(b),len(leaf_value))

					Diffuse_l = (leaf_value * b * SRF_value).sum()	/ ( SRF_sum * 3.1415 )	
					Direct_l  = (leaf_value * c * SRF_value).sum()  / ( SRF_sum * 3.1415 )	

					Diffuse_g = (grass_value * b * SRF_value).sum()	/ ( SRF_sum * 3.1415 )
					Direct_g  = (grass_value * c * SRF_value).sum() / ( SRF_sum * 3.1415 )
			
					
					test_c = np.where(M==1,Direct_l * (1 - CS ) + Diffuse_l * (1 - SCS),0)
					test_s = np.where(M==2,Direct_g * (1 - CS ) + Diffuse_g * (1 - SCS),0)

					II = test_c + test_s

					#Reflectance of virtual forest
					II = (3.1415 * II /  ( b.mean()+ c.mean() ))
					Out = II
					#i+=1
					#print(0)
				
								
				driver = gdal.GetDriverByName('GTiff')
				
				dataset = driver.Create(
					re_path+"/"+str(i_n)+"/"+B+"_"+Y_it+"_"+M_it+"_"+D_it+"_"+SZA_it+"_"+SAA_it+"_Reflectance.tif",
					Sat_x_pixels,
					Sat_y_pixels,
					3,
					gdal.GDT_Float32 , )

				dataset.SetGeoTransform((
					Sat_x_min ,  
					Sat_PIXEL_SIZE_x, 
					0,     
					Sat_y_max,   
					0,   
					Sat_PIXEL_SIZE_y))  

				dataset.GetRasterBand(1).WriteArray(CS)
				dataset.GetRasterBand(2).WriteArray(SCS)
				dataset.GetRasterBand(3).WriteArray(Out)
				dataset.FlushCache()

				dataset.FlushCache()
