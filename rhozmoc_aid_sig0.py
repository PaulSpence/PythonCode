from netCDF4 import *
from numpy import *
from scipy.stats import binned_statistic
import sys

# Overturning in rho z coords

def rhozmoc (grid_file,data_file,output_file,minval=1010,maxval=1030,inc=10):

    print 'Reading file ',grid_file
    input1 = Dataset(grid_file, 'r')
    area_t = input1.variables['area_t'][:]
    print 'area_t at 1000,100 = ',area_t[1000,1000] 

    print 'Reading file ' + data_file
    input2 = Dataset(data_file, 'r')
    rho = input2.variables['pot_rho_0'][:]
    wt = input2.variables['wt'][:]
    st_ocean = input2.variables['st_ocean'][:]
    time = input2.variables['time'][:]
    lat = input2.variables['yt_ocean'][:]
    lon = input2.variables['xt_ocean'][:]
    print 'shape rho = ',rho.shape
    print 'shape stocean = ',st_ocean.shape

    nlevels = rho.shape[1]

    # Compute transport
    wt = wt * area_t

    rhobin = arange(minval-inc*2, maxval+inc*2, inc)

    # print len(rhobin),rhobin

    # Reshape the data to only have a levels dimensions
    rho_levels = reshape(rho,(nlevels,-1))
    wt_levels = reshape(wt,(nlevels,-1))

    # Create the output data array
    ta = zeros((nlevels,size(rhobin)-1))

    # The magic happens here. The routine binned_statistic will bin rho_levels based on
    # rhobin, and then apply the statistic (sum in this case) to the similaryl shaped
    # array wt_levels. I specified min and max values so that any value outside this
    # range is ignored.
    print 'Binning'
    for i in range(nlevels):
        # print 'Level ',i
        ta[i,:], bin_edges, bin_number = binned_statistic(rho_levels[i], wt_levels[i], sum, rhobin, (min(rhobin),max(rhobin)) )

    ta = ta*1.e-6   # transport in Sv

    #sum up the transport (ta) to obtain overturning (tb)
    #in depth (depth) and density (rhobin) space
    tb = cumsum(ta,1)
    
    print "Writing output file ",output_file
    # Output to NetCDF file
    output = Dataset(output_file, 'w', format='NETCDF4')

    output.createDimension('st_ocean', nlevels)
    z_var = output.createVariable('st_ocean', 'f8', ('st_ocean',))
    z_var.units = 'meters'
    z_var[:] = st_ocean[:]

    output.createDimension('rhobin', len(rhobin)-1)
    rhobin_var = output.createVariable('rhobin', 'f8', ('rhobin',))
    rhobin_var.units = 'kg/m'
    rhobin_var[:] = rhobin[:-1]

    mx_var = output.createVariable('rho_z_trans', 'f8', ('st_ocean', 'rhobin',))
    mx_var.units = 'Sv'
    mx_var[:,:] = tb

    output.close()

    print 'finished \n'

if __name__ == "__main__":

    grid_file = '/short/v45/pas561/mom/archive/gfdl_nyf_1080/output100/ocean_grid.nc'
    data_file = '/short/v45/pas561/mom/archive/gfdl_nyf_1080/output100/ocean.nc'
    output_file = 'rho_z_moc_aid_sig0.nc'

    if len(sys.argv) == 4:
        grid_file, data_file, output_file = sys.argv[1:]
     
    rhozmoc(grid_file,data_file,output_file)
        
     

   



