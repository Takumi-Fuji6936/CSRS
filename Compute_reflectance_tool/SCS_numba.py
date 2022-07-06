import math
import numpy as np
from numba import double
from numba import jit,u2,f4,i8,i2,prange,f8,i4




@jit(i8(i8,f4,i8,f4[:],f4[:],f4[:]), nopython=True  )
def pairwise_numba(Pixel,vox_size,N_vox,X,Y,Z):

	Factor =0
	Radiance = int(Pixel/2)

	for i in range(Radiance*2):
		for j in range(Radiance*2):
			#The numver of voxels on the pixel
			Factor_pix = 0

			#Distance from center
			r_dist=math.sqrt((i- Radiance )**2+( Radiance -j)**2)	
			

			if r_dist > Radiance:
				continue
			else:			
				elevation_angle=2*math.asin(1.0*r_dist/(math.sqrt(2.0)*Radiance))				
				#print(math.degrees(elevation_angle))
				if j==Radiance and i<Radiance:
					Angle=math.pi/2
				elif j==Radiance and i>=Radiance:
					Angle = -math.pi/2
				else:
					
					Angle = math.atan2(( Radiance - i ) , ( j - Radiance ))				
					
				xa = 10*math.cos(math.pi/2-elevation_angle)*math.cos(-Angle)
				ya = 10*math.cos(math.pi/2-elevation_angle)*math.sin(-Angle)
				za = 10*math.sin(math.pi/2-elevation_angle)
				
				v11 = math.sqrt(xa**2+ya**2+za**2)
				v1_0 = xa/v11
				v1_1 = ya/v11
				v1_2 = za/v11
				
				
				

				for k in range( N_vox ):
					if Factor_pix <1:

						#Generate a cylinder
						W = ((v1_1*Z[k])-(v1_2*Y[k]))**2+((v1_2*X[k])-(v1_0*Z[k]))**2+((v1_0*Y[k])-(v1_1*X[k]))**2

						#Radius of circumscribed circle on a voxel
						r_vox = (vox_size/2*(math.sqrt(2.0)))**2

						if  W <=  r_vox  :
							Factor_pix +=1
						else:
							continue

					else:
						break
				
			Factor=Factor+Factor_pix
	return Factor



