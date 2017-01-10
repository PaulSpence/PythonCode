from netCDF4 import *
from numpy import *

# For the given simulation, calculate heat budget terms for the volume enclosed
# by the given bounds on longitude, latitude, and depth. Output as NetCDF.
# Input: base_dir = full path to simulation output directory in single quotes
#        min_year, max_year = of n in folders "outputn" inside base_dir
#        min_lon, max_lon = bounds on longitude, from -180 to 180
#        min_lat, max_lat = bounds on latitude, from -90 to 90
#        min_depth = shallowest depth in m
#        max_depth = deepest depth in m
# Example: from heatbudget import *
#          heatbudget('/short/v45/kaa561/mom/archive/gfdl_nyf_1080_AntRunoff_v2/', 101, 110, -70, -65, -75, -65, 500, 1000)

def heatbudget (base_dir, min_year, max_year, min_lon, max_lon, min_lat, max_lat, min_depth, max_depth):

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

    # Set up arrays to hold the heat budget terms (scalars) for each year
    Tadv_avg = zeros(len(time))
    TKPP_avg = zeros(len(time))
    Tsub_avg = zeros(len(time))
    Ttend_avg = zeros(len(time))
    Tvdiff_avg = zeros(len(time))
    swheat_avg = zeros(len(time))
    Ttend_theoretical = zeros(len(time))

    # Loop through the output
    for n in range(min_year, max_year+1):
        
        input_file = base_dir + 'output' + str(n) + '/ocean.nc'
        print 'Reading output' + str(n)
        input = Dataset(input_file, 'r')
        # Read vertical cell thicknesses (depends on time) and apply bounds
        dzt = input.variables['dzt'][0, min_k:max_k, min_j:max_j, min_i:max_i]
        # Read the heat budget component terms and apply bounds
        Tadv = input.variables['temp_advection'][0, min_k:max_k, min_j:max_j, min_i:max_i]
        TKPP = input.variables['temp_nonlocal_KPP'][0, min_k:max_k, min_j:max_j, min_i:max_i]
        Tsub = input.variables['temp_submeso'][0, min_k:max_k, min_j:max_j, min_i:max_i]
        Ttend = input.variables['temp_tendency'][0, min_k:max_k, min_j:max_j, min_i:max_i]
        Tvdiff = input.variables['temp_vdiffuse_diff_cbt'][0, min_k:max_k, min_j:max_j, min_i:max_i]
        swheat = input.variables['sw_heat'][0, min_k:max_k, min_j:max_j, min_i:max_i]
        input.close()

        # Calculate volume of the region by summing dzt*area over all 3 dimensions
        volume = sum(dzt*area)
        # Find the total of each term by summing term*area over all 3 dimensions
        # Find the average of each term by dividing that result by the volume
        Tadv_avg[n-min_year] = sum(Tadv*area)/volume
        TKPP_avg[n-min_year] = sum(TKPP*area)/volume
        Tsub_avg[n-min_year] = sum(Tsub*area)/volume
        Tvdiff_avg[n-min_year] = sum(Tvdiff*area)/volume
        swheat_avg[n-min_year] = sum(swheat*area)/volume
        Ttend_avg[n-min_year] = sum(Ttend*area)/volume
        # Find theoretical temperature tendency: sum of previous terms (except actual temperature tendency)
        Ttend_theoretical[n-min_year] = Tadv_avg[n-min_year] + TKPP_avg[n-min_year] + Tsub_avg[n-min_year] + Tvdiff_avg[n-min_year] + swheat_avg[n-min_year]
        # End of loop

    # Convert longitude back to normal for output
    if min_lon < -180:
        min_lon = min_lon + 360
    if max_lon < -180:
        max_lon = max_lon + 360

    # Output to NetCDF file
    output_file = base_dir + 'heatbudget_' + str(min_lon) + 'to' + str(max_lon) + '_' + str(min_lat) + 'to' + str(max_lat) + '_' + str(min_depth) + 'to' + str(max_depth) + '.nc'
    output = Dataset(output_file, 'w', format='NETCDF4')

    output.createDimension('time', None)
    time_var = output.createVariable('time', 'f8', ('time',))
    time_var[:] = time
    time_var.units = 'years'

    adv_var = output.createVariable('temp_advection', 'f8', ('time',))
    adv_var[:] = Tadv_avg
    adv_var.units = 'W/m^2'

    kpp_var = output.createVariable('temp_nonlocal_KPP', 'f8', ('time',))
    kpp_var[:] = TKPP_avg
    kpp_var.units = 'W/m^2'

    sub_var = output.createVariable('temp_submeso', 'f8', ('time',))
    sub_var[:] = Tsub_avg
    sub_var.units = 'W/m^2'

    vdiff_var = output.createVariable('temp_vdiffuse_diff_cbt', 'f8', ('time',))
    vdiff_var[:] = Tvdiff_avg
    vdiff_var.units = 'W/m^2'

    swheat_var = output.createVariable('sw_heat', 'f8', ('time',))
    swheat_var[:] = swheat_avg
    swheat_var.units = 'W/m^2'

    tend_var = output.createVariable('temp_tendency', 'f8', ('time',))
    tend_var[:] = Ttend_avg
    tend_var.units = 'W/m^2'

    tendtheor_var = output.createVariable('theoretical_temp_tendency', 'f8', ('time',))
    tendtheor_var[:] = Ttend_theoretical
    tendtheor_var.units = 'W/m^2'

    output.close()
