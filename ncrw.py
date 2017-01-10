from netCDF4 import *
from numpy import *

# For the given simulation, calculate mass transport in the x direction 
# and the corresponding barotropic streamfunction in z-space. Output as NetCDF.
# Input: base_dir = full path to simulation output directory in single quotes
#        min, max = of n in folders "outputn" inside base_dir
# Example: from mx_baropsi_z import *
#          mx_baropsi_z('/short/v45/kaa561/mom/archive/gfdl_nyf_1080_AntRunoff_v2/', 101, 110)

def ncrw (in_dir,out_dir):

    # Open the first output
    input_file = in_dir + '/t4_10.nc'
    output_file = out_dir + '/t_10.nc'
    print 'Reading file' + input_file
    print 'Writing file' + output_file
    
    input = Dataset(input_file, 'r')
    temp = input.variables['T_10'][:,:,:]
    print input.variables['T_10']
    print 'Temp at 100,100,100=\n ',temp[100,1000,1000] 
    print 'Writing file' + output_file

    # Output to NetCDF file
    output = Dataset(output_file, 'w', format='NETCDF4')

    x_var = output.variable['T_10'][:,:,:]=temp
    output.close()
    
    #if __name__ == "__main":
    #    mx_baropsi_z('/g/data1/v45/pas561/mom/core_nyf/gfdl_nyf_1080/',180,210)    



