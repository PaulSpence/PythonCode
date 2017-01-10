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
min_depth=0
max_depth=5000
varname='salt'

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
min_k = nonzero(depth > min_depth)[0][0]
max_k = nonzero(depth > max_depth)[0][0]


area=area[min_j:max_j, min_i:max_i]


input = Dataset('../gfdl_nyf_1080/output101/ocean.nc', 'r')
var = input.variables[varname][0, min_k:max_k, min_j:max_j, min_i:max_i]
dzt = input.variables['dzt'][0, min_k:max_k, min_j:max_j, min_i:max_i]
input.close()  

	        
var_avg = sum(var*area*dzt)/sum(area*dzt)
print 'var 3D avg ' + str(var_avg)


