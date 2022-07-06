import math
import numpy as np
from time import sleep
from tqdm import tqdm
import time
import traceback
from Compute_reflectance_tool import SCS_numba


def loop(TT,Pixel,Vox_size,N,start,end,X,Y,Z,i):
	#Coordinate of target voxel
	x0 = X[i]
	y0 = Y[i]
	z0 = Z[i]
	Int = 0
	if x0 > Int  and x0 <TT- Int and y0 > Int and y0 < TT - Int: 

		XX = np.delete(X,i)
		YY = np.delete(Y,i)
		ZZ = np.delete(Z,i)

		Xa = XX[ZZ>z0]
		Ya = YY[ZZ>z0]
		Za = ZZ[ZZ>z0]

		X_x0 = (Xa - x0)
		Y_y0 = (Ya - y0)
		Z_z0 = (Za - z0)

		# Dist =np.round(np.sqrt( X_x0**2 + Y_y0**2 + Z_z0**2 ),decimals=3)
		
		# #Extract voxels which are less than 5.0 m distance to target voxel  
		# index = np.where(Dist<=20.0)
		
		# #Extract voxel cooridinate
		# X_ex = X_x0[index]
		# Y_ex = Y_y0[index]
		# Z_ex = Z_z0[index]

		N_vox = len(Za)

		SVF = SCS_numba.pairwise_numba(Pixel,Vox_size,N_vox,X_x0,Y_y0,Z_z0)


	else:
		SVF = -6360


	return SVF