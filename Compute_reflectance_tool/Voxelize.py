import pandas as pd
import sys
import numpy as np
from tqdm import tqdm
from time import sleep
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
import glob
import re
import os


def Voxelize(files,new_path,Voxel_size):
	for f in files:
		print(f)

		name = re.split('[/.]',f)[-2]
		print(name)
		
		data = pd.read_csv(f,delim_whitespace=True)
		
		n = len(data.index)
		
		voxel_interval = Voxel_size

		xmin = round(min(data["x"]),3)
		ymin = round(min(data["y"]),3)
		zmin = round(min(data["z"]),3)

		#print(xmin,ymin,zmin)

		start_voxel_center_x = round( xmin + ( voxel_interval / 2 ) , 3 )
		start_voxel_center_y = round( ymin + ( voxel_interval / 2 ) , 3 )
		start_voxel_center_z = round( zmin + ( voxel_interval / 2 ) , 3 )

		x_row = data["x"].map(lambda x: float(Decimal(str(x))
												.quantize(Decimal("0.001"),rounding=ROUND_HALF_UP)))

		y_row = data["y"].map(lambda x: float(Decimal(str(x))
												.quantize(Decimal("0.001"),rounding=ROUND_HALF_UP)))

		z_row = data["z"].map(lambda x: float(Decimal(str(x))
												.quantize(Decimal("0.001"),rounding=ROUND_HALF_UP)))

		#Voxel coordinate
		data['xnum'] = np.floor( ( x_row -xmin)/voxel_interval )
		data['ynum'] = np.floor( ( y_row -ymin)/voxel_interval )
		data['znum'] = np.floor( ( z_row -zmin)/voxel_interval )


		df = data
		df = df.sort_values(['xnum','ynum','znum'], ascending=[True,True,True])
		df = df.reset_index(drop=True)
		
		xnum=np.array(df['xnum'])
		ynum=np.array(df['ynum'])
		znum=np.array(df['znum'])


		x  = np.array(df['x'])
		y  = np.array(df['y'])
		z  = np.array(df['z'])
		id_ = np.array(df['Tree_ID'])
		mate_ = np.array(df['material'])
		
		nx = np.array(df['Nx'])
		ny = np.array(df['Ny'])
		nz = np.array(df['Nz'])

		X  = x[0]
		Y  = y[0]
		Z  = z[0]
		ID = id_[0]
		MT = mate_[0]

		NX=nx[0]
		NY=ny[0]
		NZ=nz[0]

		N=len(df['ynum'])

		k=1
		f=open( new_path+"/"+ name +"_vox.txt",mode="w" )
		for i in tqdm(range(1,N)):
			
			if xnum[i-1]==xnum[i] and ynum[i-1]==ynum[i] and znum[i-1]==znum[i]:
								
				X = X+x[i]
				Y = Y+y[i]
				Z = Z+z[i]

				ID = ID+id_[i]

				MT = MT+mate_[i]

				NX = NX+nx[i]
				NY = NY+ny[i]
				NZ = NZ+nz[i]
				
				k+=1
				#if i==n-1 :
				#	xp_centar=xmin+voxel_center+xnum[i]*voxel_interval
					#yp_centar=ymax+voxel_center+ynum[i]*voxel_interval
					
					#print round(xp_centar,3),round(yp_centar,3),X/k,Y/k,Z/k,R/k,G/k,B/k,k
					#print round(xp_centar,3),round(yp_centar,3),k
			else:
				xp_centar = round( start_voxel_center_x + xnum[i-1]*voxel_interval,2)
				yp_centar = round( start_voxel_center_y + ynum[i-1]*voxel_interval,2)
				zp_centar = round( start_voxel_center_z + znum[i-1]*voxel_interval,2)

				Xx  = round(X/k,3)
				Yy  = round(Y/k,3)
				Zz  = round(Z/k,3)
				IID = int(ID/k+0.5) 
				NXx = round(NX/k,3)
				NYy = round(NY/k,3)
				NZz = round(NZ/k,3)

				MTT = int(MT/k+0.5)

				print ( xp_centar, yp_centar, zp_centar,Xx,Yy,Zz,NXx,NYy,NZz,IID,MTT,file=f)
				

				k = 1
				
				
				X  = x[i]
				Y  = y[i]
				Z  = z[i]
				ID = id_[i]
				NX = nx[i]
				NY = ny[i]
				NZ = nz[i]
				MT = mate_[i]


				#if i==n-1 :
				#	xp_centar=xmin+voxel_center+xnum[i]*voxel_interval
					#yp_centar=ymax+voxel_center+ynum[i]*voxel_interval
					
					#print round(xp_centar,3),round(yp_centar,3),X/k,Y/k,Z/k,R/k,G/k,B/k,k


		f.close()
