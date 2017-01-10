from netCDF4 import *
from numpy import *

# For the given simulation, calculate heat budget advection terms for the volume enclosed by the given bounds on longitude, latitude, and depth. Output as NetCDF.
# Input: base_dir = full path to simulation output directory in single quotes
#        min_year, max_year = of n in folders "outputn" inside base_dir
#        min_lon, max_lon = bounds on longitude, from -180 to 180
#        min_lat, max_lat = bounds on latitude, from -90 to 90
#        min_depth = shallowest depth in m
#        max_depth = deepest depth in m
# Example: from heatbudget_adv import *
#          heatbudget_adv('/short/v45/kaa561/mom/archive/gfdl_nyf_1080_AntRunoff_v2/', 101, 110, -70, -65, -75, -65, 500, 1000)

def heatbudget_adv (base_dir, min_year, max_year, min_lon, max_lon, min_lat, max_lat, min_depth, max_depth):

    time = range(min_year, max_year+1)

    # Read the area of tracer grid cells
    input_file = base_dir + 'output' + str(min_year) + '/ocean_grid.nc'
    input = Dataset(input_file, 'r')
    area = input.variables['area_t'][:,:]
    input.close()

    # Read the longitude, latitude, and depth
    input_file = base_dir + 'output' + str(min_year) + '/ocean.nc'
    input = Dataset(input_file, 'r')
    lon = input.variables['xt_ocean'][:]
    lat = input.variables['yt_ocean'][:]
    depth = input.variables['st_ocean'][:]
    input.close()

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

    # Apply these bounds to the area array
    area = area[min_j:max_j, min_i:max_i]

    # Set up arrays to hold the heat budget advection terms (scalars) for each year
    Tadvx_avg = zeros(len(time))
    Tadvy_avg = zeros(len(time))
    Tadvz_avg = zeros(len(time))
    Tadv_avg = zeros(len(time))
    Tadv_theoretical = zeros(len(time))

    # Loop through the output
    for n in range(min_year, max_year+1):

        input_file = base_dir + 'output' + str(n) + '/ocean.nc'
        print 'Reading output' + str(n)
        input = Dataset(input_file, 'r')
        # Read vertical cell thicknesses (depends on time) and apply bounds
        dzt = input.variables['dzt'][0, min_k:max_k, min_j:max_j, min_i:max_i]
        # Read temperature advection flux in the x direction, subtracting opposite faces. This is equivalent to the sum over i of Tadvx[k,j,i] - Tadvx[k,j,i-1]
        Tadvx_flux = input.variables['temp_xflux_adv'][0, min_k:max_k, min_j:max_j, min_i+1:max_i] - input.variables['temp_xflux_adv'][0, min_k:max_k, min_j:max_j, min_i:max_i-1]
        # Similarly for the y direction: Tadvy[k,j,i] - Tadvy[k,j-1,i]
        Tadvy_flux = input.variables['temp_yflux_adv'][0, min_k:max_k, min_j+1:max_j, min_i:max_i] - input.variables['temp_yflux_adv'][0, min_k:max_k, min_j:max_j-1, min_i:max_i]
        # For the z direction, opposite sign: Tadvz[k-1,j,i] - Tadvz[k,j,i]
        Tadvz_flux = input.variables['temp_zflux_adv'][0, min_k:max_k-1, min_j:max_j, min_i:max_i] - input.variables['temp_zflux_adv'][0, min_k+1:max_k, min_j:max_j, min_i:max_i]
        # Also read the temperature advection
        Tadv = input.variables['temp_advection'][0, min_k:max_k, min_j:max_j, min_i:max_i]
        input.close()

        # Calculate volume of the region by summing dzt*area over all 3 dimensions
        volume = sum(dzt*area)
        # Find the total temperature advection in each direction by summing over all 3 dimensions
        # Find the average temperature advection in each direction by dividing that result by the volume
        Tadvx_avg[n-min_year] = sum(Tadvx_flux)/volume
        Tadvy_avg[n-min_year] = sum(Tadvy_flux)/volume
        Tadvz_avg[n-min_year] = sum(Tadvz_flux)/volume
        # Since the temperature advection is in W/m^2 not W, need to multiply by area before summing and dividing by volume
        Tadv_avg[n-min_year] = sum(Tadv*area)/volume
        # Find theoretical temperature advection: sum of each direction
        Tadv_theoretical[n-min_year] = Tadvx_avg[n-min_year] + Tadvy_avg[n-min_year] + Tadvz_avg[n-min_year]
        # End of loop

    # Output to NetCDF file
    output_file = base_dir + 'heatbudgetadv_' + str(min_lon) + 'to' + str(max_lon) + '_' + str(min_lat) + 'to' + str(max_lat) + '_' + str(min_depth) + 'to' + str(max_depth) + '.nc'
    output = Dataset(output_file, 'w', format='NETCDF4')

    output.createDimension('time', None)
    time_var = output.createVariable('time', 'f8', ('time',))
    time_var[:] = time
    time_var.units = 'years'

    advx_var = output.createVariable('temp_advection_x', 'f8', ('time',))
    advx_var[:] = Tadvx_avg
    advx_var.units = 'W/m^2'

    advy_var = output.createVariable('temp_advection_y', 'f8', ('time',))
    advy_var[:] = Tadvy_avg
    advy_var.units = 'W/m^2'

    advz_var = output.createVariable('temp_advection_z', 'f8', ('time',))
    advz_var[:] = Tadvz_avg
    advz_var.units = 'W/m^2'

    adv_var = output.createVariable('temp_advection', 'f8', ('time',))
    adv_var[:] = Tadv_avg
    adv_var.units = 'W/m^2'

    advtheor_var = output.createVariable('theoretical_temp_advection', 'f8', ('time',))
    advtheor_var[:] = Tadv_theoretical
    advtheor_var.units = 'W/m^2'

    output.close()
