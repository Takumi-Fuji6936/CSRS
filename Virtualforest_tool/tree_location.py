import numpy as np
import math
import pandas as pd
import random

def tree_location(Forest_scale,CC,TH_ave,TH_std,Slope,Asym_it,CR_ave,CR_std,dbh):
	
	#Initial tree coordinate
	Location_list = np.arange(0,Forest_scale,0.1)
	x_0 = random.choice(Location_list)
	y_0 = random.choice(Location_list)

	Slope = math.radians(Slope)

	#Tree heigt
	TH_0 = random.normalvariate(TH_ave,TH_std) 
	#Crown radius
	r = random.normalvariate(CR_ave, CR_std)
	#Crown length
	cl = TH_0 / 2


	xc = np.array(x_0)
	yc = np.array(y_0)
	H  = np.array(TH_0)

	DBH = np.array(dbh)
	R  = np.array(r)
	CL = np.array(cl)
	RRR = np.array(0)
	
	#Percent overlap with neighboring trees
	#Initial value is 0.1
	Over = 0.1

	x_it = np.arange(0,Forest_scale,0.1)
	y_it = np.arange(0,Forest_scale,0.1)

	
	#樹冠カバー率の計算
	count = 0
	location = 0

	initial = 0

	Test = np.arange((Forest_scale/0.1)**2)


	#Prepare an array to store tree locations
	#Initial tree position is greater than or equal to 0, so initialized at -1
	L_2d = -1 * np.ones(80000)

	before_j  = 0
	before_cc = 0

	for tx in range(len(x_it)):
		xx = x_it[tx]

		for ty in range(len(y_it)):
			yy = y_it[ty]

			x_c = xc
			y_c = yc
			r_c = R

			if yy < (y_c + ( R * Asym_it )):
				#Check whether xx and yy are inside a circle of radius r_c at center position (x_c,y_c)
				yyy = (x_c - xx)**2 + (y_c - yy)**2 - r_c**2 

				if yyy<0:
					count+=1

					if initial == 0:
						count_array = 0

						L_2d[count_array] = location

						initial+=1
						count_array+=1

					elif initial != 0:
						#print(location)

						L_2d[count_array] = location
						count_array+=1
				else:
					pass
			else:
				pass

			location+=1	

	#Calculation of canopy coverage
	CCC = count / len(x_it)**2
	print( 0,"CC", CCC )

	
	#Remove 0 or less from L_2d
	bbb = L_2d[~(L_2d <=0)]
	#print(L_2d)

	Test = np.setdiff1d(Test,bbb)

	#Calculate the tree location
	#Increase the allowable tree overlap ratio as the for statement progresses to reduce computational cost.
	Num_of_tree = 1
	for i in range(1,2000):

		if i > 50:
			Over = 0.2

		elif i > 100:
			Over = 0.3

		elif i > 150:
			Over = 0.4

		elif i > 200:
			Over = 0.7

		elif i > 250:
			Over = 0.7

		
		L = -1 * np.ones(80000)

		#Increase number of trees until CCC exceeds CC/100
		if CCC > CC/100:
			break

		seed = np.random.choice(Test)

		x_y = divmod(seed,(Forest_scale/0.1))

		new_x = x_y[0]*0.1
		new_y = x_y[1]*0.1
		#print(new_x,new_y)

		new_TH = random.normalvariate(TH_ave,TH_std) 

		ddbh = dbh

		radius = random.normalvariate(CR_ave, CR_std)

		ccl = new_TH / 2

		count = 0
		location = 0
		initial = 0
		for tx in range(len(x_it)):
			xx = x_it[tx]

			for ty in range(len(y_it)):
				yy = y_it[ty]

				x_c = new_x
				y_c = new_y
				r_c = radius

				if yy < (y_c + ( r_c * Asym_it )):
					yyy = (x_c - xx)**2 + (y_c - yy)**2 - r_c**2 

					if yyy<0:
						count+=1
						
						if initial == 0:
							count_array = 0
							L[count_array] = location

							initial+=1
							count_array+=1

						elif initial != 0:
							L[count_array] = location
							count_array+=1

					else:
						pass
				else:
					pass

				location+=1	


		#print('aaaaaa')
		if Num_of_tree == 1:

			Decided = L_2d[~(L_2d <=0)]

			check = L[~(L <=0)]
			duplicate = np.intersect1d(Decided, check)

			if len(duplicate)/len(Decided) < Over :

				AAA = np.union1d(Decided,check)
				
				CCC = len(AAA) / len(x_it)**2

				L_2d = np.vstack((L_2d,L))

				Test = np.setdiff1d(Test,check)


				Num_of_tree+=1


		

		elif Num_of_tree>1:
			TTT = 0

			check = L[~(L <=0)]

			for j in range(Num_of_tree):

				Decided = L_2d[j][~(L_2d[j] <=0)]

				duplicate = np.intersect1d(Decided, check)

				#print(Decided)
				if len(Decided) <= 0:
					continue

				if len(duplicate)/len(Decided) > Over:
					#print("overlap")
					TTT = 1
					break

				elif len(duplicate)/len(Decided) <= Over :
					continue


			if TTT == 0:

				AAA = np.union1d(L_2d[0:Num_of_tree+1],check)
			
				CCC = len(AAA) / len(x_it)**2
				#print(AAA)
				
				after_j = j
				after_cc = CCC

				if after_cc > before_cc:
					#print(before_cc,after_cc)

					before_cc = after_cc
					print(i, j,"CC", CCC )

					xc = np.append(xc,new_x)
					yc = np.append(yc,new_y)
					R  = np.append(R,radius)
					H  = np.append(H,new_TH)
					DBH =np.append(DBH,ddbh)
					CL = np.append(CL,ccl)


					L_2d = np.vstack((L_2d,L))
					#print(L_2d)

					Test = np.setdiff1d(Test,check)


					Num_of_tree+=1

	#print(i, j,"CC", CCC )
	zc = math.sin(Slope) * yc
	#print(yc)
	print(CC,CCC)
	return CCC,0,0,xc,yc,zc,R,H,DBH,CL



if __name__ == "__main__":
   main()