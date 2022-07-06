import math
import numpy as np
import numpy.random as rd
import random

def model_func(x, a, k, b):
    return a * np.exp(-k*x) + b

def fai_theta(Voxel_size,CR,N):
	#CR = np.arange(3,10,0.5)
	Opti_inter = np.zeros(len(CR))
	Opti_test = np.zeros(len(CR))
	Finish = N
	DD = Voxel_size*0.75
	Y = np.zeros(len(CR))
	i_Y = 0
	for i_CR in CR:

		for i in range(Finish):
			inverse = ((Finish - i) / 1000)
			fai = math.radians( inverse )

			diff = math.sqrt( (i_CR - i_CR * math.cos(fai))**2 + ( i_CR * math.sin(fai) )**2 )

			if diff < DD:
				Y[i_Y] = (360/inverse)*2
				Opti_inter[i_Y] = fai
				Opti_test[i_Y] = ((2*math.pi)/fai)*(math.pi/fai)
				#print(i_CR,inverse,round(diff,5),(360/inverse))
				break
		i_Y+=1
	#print(Opti_test)
	return Opti_inter
 