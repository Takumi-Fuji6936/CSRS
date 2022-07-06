import math
import numpy as np
import pandas as pd
import sys
from time import sleep
from tqdm import tqdm
import time
import threading
import traceback
from Compute_reflectance_tool import SCS_loop
from multiprocessing import Pool
from multiprocessing import Process
from joblib import Parallel, delayed
from time import sleep
from tqdm import tqdm
import time
import glob
import re
import os


def SCS_main(files,new_path,Forest_scale,VS,core_n):

	t = time.time()
	Vox_size = VS
	TT = Forest_scale
	Pixel = 90
	start = 0
	
	
	for f in files:
		
		f_name = re.split('[/.]',f)[-2]
		print(f_name)
		
		data = pd.read_csv(f,delim_whitespace=True,names=("x","y","z","xx","yy","zz","Nx","Ny","Nz","ID","Material"))
		
		data=data.drop_duplicates(['x','y','z'])
	
		N =len(data.index)
		print(N)
		end   = int(N)

		X = np.array(data['x']).astype(np.float32)
		Y = np.array(data['y']).astype(np.float32)
		Z = np.array(data['z']).astype(np.float32)
		SVF = np.zeros(N).astype(np.float32)
		
		SCS_compute = np.array(Parallel(n_jobs=core_n,verbose=2)( [ delayed(SCS_loop.loop)(TT,Pixel,Vox_size,N,start,end,X,Y,Z,i) for i in tqdm(range (start,end))] ))
		
		data["SCS"] = np.round(SCS_compute/6360,4)

		data.to_csv(new_path+"/"+ f_name+"_SCS.txt",index=False,sep=" ")
		print( time.time()-t)
	