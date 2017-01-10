from netCDF4 import *
from numpy import *

# For the given simulation, calculate mass transport in the x direction 
# and the corresponding barotropic streamfunction in z-space. Output as NetCDF.
# Input: base_dir = full path to simulation output directory in single quotes
#        min, max = of n in folders "outputn" inside base_dir
# Example: from mx_baropsi_z import *
#          mx_baropsi_z('/short/v45/kaa561/mom/archive/gfdl_nyf_1080_AntRunoff_v2/', 101, 110)

def mx_baropsi_z (base_dir, min, max):

    # Assume time is year min to year max
    time = range(min, max+1)

    # Open the first output
    input_file = base_dir + 'output' + str(min) + '/ocean.nc'
    print 'Reading output' + str(min)
    input = Dataset(input_file, 'r')
    # Read the longitude and latitude
    lon = input.variables['xu_ocean'][:]
    lat = input.variables['yu_ocean'][:]
    dimensions_2d = (len(time), len(lat), len(lon))
    # Read tx_trans; missing values are automatically masked
    tx_trans = input.variables['tx_trans'][0,:,:,:]
    # Save the land-sea mask for later
    tx_trans_2d = tx_trans[0,:,:]
    land_sea = ones(shape(tx_trans_2d))
    index = tx_trans_2d.mask
    land_sea[index] = NaN
    # Set up mass transport array along time, latitude, longitude dimensions
    mass_transport = zeros(dimensions_2d)
    # Vertical sum of tx_trans to get mass transport
    mass_transport[0,:,:] = sum(tx_trans, axis=0)
    input.close()

    # Loop through the rest of the output
    for n in range(min+1, max+1):
        input_file = base_dir + 'output' + str(n) + '/ocean.nc'
        print 'Reading output' + str(n)
        input = Dataset(input_file, 'r')
        # Read tx_trans; missing values are automatically masked
        tx_trans = input.variables['tx_trans'][0,:,:,:]
        mass_transport[n-min,:,:] = sum(tx_trans, axis=0)
        input.close()

    # Set up streamfunction array along time, latitude, longitude dimensions
    baro_psi = zeros(dimensions_2d)
    # Cumulative sum of mass transport from south to north
    baro_psi[:,0,:] = mass_transport[:,0,:]
    for j in range(1, len(lat)):
        baro_psi[:,j,:] = baro_psi[:,j-1,:] + mass_transport[:,j,:]

    # Mask out the land in output fields: multiply by mask which is 1 on
    # ocean cells, NaN on land cells
    mass_transport = mass_transport*land_sea
    baro_psi = baro_psi*land_sea

    # Output to NetCDF file
    output_file = base_dir + 'mx_baropsi_z.nc'
    output = Dataset(output_file, 'w', format='NETCDF4')

    output.createDimension('time', None)
    time_var = output.createVariable('time', 'f8', ('time',))
    time_var[:] = time
    time_var.units = 'years'

    output.createDimension('latitude', len(lat))
    lat_var = output.createVariable('latitude', 'f8', ('latitude',))
    lat_var[:] = lat
    lat_var.units = 'degrees north'

    output.createDimension('longitude', len(lon))
    lon_var = output.createVariable('longitude', 'f8', ('longitude',))
    lon_var[:] = lon + 100
    lon_var.units = 'degrees east'

    mx_var = output.createVariable('mass_transport_x', 'f8', ('time', 'latitude', 'longitude',))
    mx_var[:,:,:] = mass_transport
    mx_var.units = 'Sv'

    psi_var = output.createVariable('baro_psi', 'f8', ('time', 'latitude', 'longitude',))
    psi_var[:,:,:] = baro_psi
    psi_var.units = 'Sv'

    output.close()
    
    #if __name__ == "__main":
    #    mx_baropsi_z('/g/data1/v45/pas561/mom/core_nyf/gfdl_nyf_1080/',180,210)    



