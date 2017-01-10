from netCDF4 import *
from numpy import *

# For the given simulation, calculate mass transport in the y direction 
# and the corresponding barotropic streamfunction in density space. Output as NetCDF.
# Input: base_dir = full path to simulation output directory in single quotes
#        min, max = of n in folders "outputn" inside base_dir
# Example: run my_baropsi_rho('/short/v45/pas561/mom/archive/gfdl_nyf_1080/', 201, 210)

def my_baropsi_rho (base_dir, min, max):

    # Assume time is year min to year max
    time = range(min, max+1)

    # Open the first output
    input_file = base_dir + 'output' + str(min) + '/ocean.nc'
    print 'Reading output' + str(min)
    input = Dataset(input_file, 'r')
    # Read the latitude and potential density
    lat = input.variables['yu_ocean'][:]
    rho = input.variables['potrho'][:]
    dimensions_2d = (len(time), len(rho), len(lat))
    # Read ty_trans_rho; missing values are automatically masked
    ty_trans_rho = input.variables['ty_trans_rho'][0,:,:,:]
    # Set up mass transport array along time, density, latitude dimensions
    mass_transport = zeros(dimensions_2d)
    # Zonal sum of ty_trans_rho to get mass transport
    mass_transport[0,:,:] = sum(ty_trans_rho, axis=2)
    input.close()

    # Loop through the rest of the output
    for n in range(min+1, max+1):
        input_file = base_dir + 'output' + str(n) + '/ocean.nc'
        print 'Reading output' + str(n)
        input = Dataset(input_file, 'r')
        # Read ty_trans_rho and do zonal sum to get mass transport
        ty_trans_rho = input.variables['ty_trans_rho'][0,:,:,:]
        mass_transport[n-min,:,:] = sum(ty_trans_rho, axis=2)
        input.close()

    # Set up streamfunction array along time, density, latitude dimensions
    baro_psi = zeros(dimensions_2d)
    # Cumulative vertical sum of mass transport from top to bottom
    baro_psi[:,0,:] = mass_transport[:,0,:]
    for k in range(1, len(rho)):
        baro_psi[:,k,:] = baro_psi[:,k-1,:] + mass_transport[:,k,:]

    # Output to NetCDF file
    output_file = base_dir + 'my_baropsi_rho.nc'
    output = Dataset(output_file, 'w', format='NETCDF4')

    output.createDimension('time', None)
    time_var = output.createVariable('time', 'f8', ('time',))
    time_var[:] = time
    time_var.units = 'years'

    output.createDimension('potential_density', len(rho))
    rho_var = output.createVariable('potential_density', 'f8', ('potential_density',))
    rho_var[:] = rho
    rho_var.units = 'kg/m^3'

    output.createDimension('latitude', len(lat))
    lat_var = output.createVariable('latitude', 'f8', ('latitude',))
    lat_var[:] = lat
    lat_var.units = 'degrees north'

    mx_var = output.createVariable('mass_transport_y', 'f8', ('time', 'potential_density', 'latitude',))
    mx_var[:,:,:] = mass_transport
    mx_var.units = 'Sv'

    psi_var = output.createVariable('baro_psi', 'f8', ('time', 'potential_density', 'latitude',))
    psi_var[:,:,:] = baro_psi
    psi_var.units = 'Sv'

    output.close()
    
    



