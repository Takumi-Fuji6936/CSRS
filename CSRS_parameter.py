Dir          = 'Test'  #Name of directory to store virtual forests.
Forest_scale = 40      #Size of virtual forest(m)
Voxel_size   = 0.5     #Voxel size(m)
CC           = 50      #Crown coverage(persentage)
#Tree height and crown radius are followed normal distribution.
#Crown length is half of tree height.
th_ave       = 7       #Average tree height(m)
th_std       = 2       #Standard deviation of tree height(m)
cr_ave       = 4       #Average crown radius(m)
cr_std       = 2       #Standard deviation of crown radius(m)
dbh          = 0.3     #Diameter at breast height(m)
n            = 2       #Number of virtual forest of each canopy shape
slope        = 0       #Slope of virtual forest(degree)
core_n       = 4       #Number of CPUs for parallel processing
shape        = 0       #Target canopy shape to calculate reflectance. 
#shape list  = {0:"Ellipsoid",1:"Ellipsoid_half",2:"Ellipsoid_half_upside_down",
# 			3:"Cylinder"}
#Note, Create_reflectance.py generate virtual forest in all canopy shapes (0 to 3).
#Compute_reflectance.py calculate the reflectance in the canopy shape which you choose in "shape" parameter.
Sun_geometry = "Parameter/sun_geometry.txt" # Sun geometry file. The file required 'Year', 'Date', 'SAA' and 'SZA'.
Lambda       = 'Parameter/Lambda.csv'  # Define band width of target satellite sensor.
SRF          = 'Parameter/Sensor_SRF/SRF_S2A.csv' #Spectral responce function of target satellite sensor.
canopy       = 'Parameter/SR/canopy.txt' #Spectral reflectance of leaf
floor        = 'Parameter/SR/floor.txt' #Spectral reflectance of grass
irradiance   = 'Parameter/Irradiance' #Solar irradiance of each band.
