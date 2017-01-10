from netCDF4 import *
from numpy import *

# For the given simulation, calculate heat budget terms for the volume enclosed
# by the given bounds on longitude, latitude, and depth. Output as NetCDF.
# Input: base_dir = full path to simulation output directory in single quotes
#        variable to be averaged: e.g. temp
#        min_year, max_year = of n in folders "outputn" inside base_dir
#        min_lon, max_lon = bounds on longitude, from -180 to 180
#        min_lat, max_lat = bounds on latitude, from -90 to 90
#        min_depth = shallowest depth in m
#        max_depth = deepest depth in m
# Example: from heatbudget import *
#          heatbudget('/short/v45/kaa561/mom/archive/gfdl_nyf_1080_AntRunoff_v2/', 101, 110, -70, -65, -75, -65, 500, 1000)


input = Dataset('../gfdl_nyf_1080/output101/ocean_grid.nc', 'r')
area = input.variables['area_t'][:,:]
input.close()


# Read the heat budget component terms and apply the bounds on i, j, k
input = Dataset('../gfdl_nyf_1080/output101/ocean.nc', 'r')
lon = input.variables['xt_ocean'][:]
lat = input.variables['yt_ocean'][:]
depth = input.variables['st_ocean'][:]
input.close()

min_lon=-73
max_lon=-67
min_lat=-70.5
max_lat=-65.5
varname='sea_level'
min_year=201
max_year=205
base_dir='/short/v45/pas561/mom/archive/gfdl_nyf_1080_PI_Ant_20Eto140E/1yr_5day/'

# Convert the bounds on longitude so they work with grid (-280 to 80)
if min_lon > 80:
	min_lon = min_lon - 360
if max_lon > 80:
	max_lon = max_lon - 360
if max_lon < min_lon:
	print 'Invalid longitude bounds; grid splits at 80E'

# Find the smallest value of i such that lon[i] > min_lon
min_i = nonzero(lon > min_lon)[0][0]
# Find the smallest value of i such that lon[i] > max_lon
# In practice the actual maximum index selected by min_i:max_i will be max_i - 1
max_i = nonzero(lon > max_lon)[0][0]
# Similarly for j (latitude) and k (depth)
min_j = nonzero(lat > min_lat)[0][0]
max_j = nonzero(lat > max_lat)[0][0]

area=area[min_j:max_j, min_i:max_i]

time = range(min_year, max_year+1)



#set up arrays to hold the heat budget terms (scalars) for each year
var_avg = zeros(len(time)*73)

# Loop through the output    for n in range(min_year, max_year+1):
cnt=0
for n in range(min_year, max_year+1):
	for d in range(3,364,5):
		if d < 10:
        		input_file= base_dir + 'output' + str(n) + '/ocean__' + str(n) + '_00' + str(d) + '.nc'
        	elif d < 100:
        		input_file= base_dir + 'output' + str(n) + '/ocean__' + str(n) + '_0' + str(d) + '.nc'
        	else:
        		input_file= base_dir + 'output' + str(n) + '/ocean__' + str(n) + '_' + str(d) + '.nc'

                cnt=cnt+1
        	print 'Reading output' + input_file + ' cnt ' + str(cnt)

        	input = Dataset(input_file, 'r')
        	# Read the heat budget component terms and apply the bounds on i, j, k
		var = input.variables[varname][0, min_j:max_j, min_i:max_i]
		input.close()  

        	# Find the total of each term by summing term*area over all 3 dimensions
        	# Find the average of each term by dividing that result by the volume
		var_avg[cnt-1] = sum(var*area)/sum(area)
		print 'var 3D avg ' + str(var_avg[cnt-1])
        	# End of loop

# Convert longitude back to normal for output
if min_lon < -180:
	min_lon = min_lon + 360
if max_lon < -180:
	max_lon = max_lon + 360

# Output to NetCDF file
output_file = base_dir + str(varname) +'_2Davg_' + str(min_year) +'to'+ str(max_year) + '_' + str(min_lon) + 'to' + str(max_lon) + '_' + str(min_lat) + '.nc'
output = Dataset(output_file, 'w', format='NETCDF4')

output.createDimension('time', None)
time_var = output.createVariable('time', 'f8', ('time',))
time_var[:] = range(len(time)*73)
time_var.units = 'years'

adv_var = output.createVariable(str(varname), 'f8', ('time',))
adv_var[:] = var_avg
adv_var.units = 'variable'

output.close()



