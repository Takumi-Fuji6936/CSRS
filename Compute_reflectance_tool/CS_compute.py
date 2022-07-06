import math
import numpy as np
from numba import double
from numba import jit,u2,f4,i2,u1,prange,i8

@jit(u2[:](f4[:],f4[:],f4[:],f4,f4,f4,u2[:],i8,f4), nopython=True,parallel=True)
def pairwise_numba(X,Y,Z,a,b,c,DD_1,N,VOXEL_SIZE):

	#print(N)
	d=VOXEL_SIZE/4
	dd=VOXEL_SIZE/2
	Count=0
	DD_2=np.copy(DD_1)
	DD_3=np.copy(DD_1)
	DD_4=np.copy(DD_1)

	for i in prange(N):
		XX = np.zeros(4)
		YY = np.zeros(4)
		#print(i)

		X_0=X[i]
		Y_0=Y[i]
		Z_0=Z[i]
		
		XX[0],XX[1],XX[2],XX[3]=X_0-d,X_0+d,X_0-d,X_0+d
		YY[0],YY[1],YY[2],YY[3]=Y_0+d,Y_0+d,Y_0-d,Y_0-d
		
		for j in range(N):
			X_c= X[j]
			Y_c= Y[j]
			Z_ave= Z[j]
			

			if Z_ave>Z_0 :
				t=( Z_ave - Z_0 ) / c

				
				xx_1= a * t + XX[0]
				yy_1= b * t + YY[0]

				if DD_1[i]<1 and xx_1>X_c-dd and xx_1<X_c+dd and yy_1>Y_c-dd and yy_1<Y_c+dd:
					DD_1[i]+=1

				xx_2= a * t + XX[1]
				yy_2= b * t + YY[1]

				if DD_2[i]<1 and xx_2>X_c-dd and xx_2<X_c+dd and yy_2>Y_c-dd and yy_2<Y_c+dd:
					DD_2[i]+=1

				xx_3= a * t + XX[2]
				yy_3= b * t + YY[2]

				if DD_3[i]<1 and xx_3>X_c-dd and xx_3<X_c+dd and yy_3>Y_c-dd and yy_3<Y_c+dd:
					DD_3[i]+=1

				xx_4= a * t + XX[3]
				yy_4= b * t + YY[3]		

				if DD_4[i]<1 and xx_4>X_c-dd and xx_4<X_c+dd and yy_4>Y_c-dd and yy_4<Y_c+dd:	
					DD_4[i]+=1




			else:
				continue
			
		
	return DD_1+DD_2+DD_3+DD_4

