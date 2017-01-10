from netCDF4 import *
from numpy import *

# Overturning in rho z coords

def rhozmoc (data_file,grid_file):

   
    #tx_trans = input.variables['tx_trans'][0,:,:,:]
    #mass_transport[n-min,:,:] = sum(tx_trans, axis=0)
    
    data_file = '/short/v45/pas561/mom/archive/gfdl_nyf_1080/output201/ocean.nc'
    grid_file = '/short/v45/pas561/mom/archive/gfdl_nyf_1080/output201/ocean_grid.nc'
     
    print 'Reading file ' + grid_file
    input1 = Dataset(grid_file, 'r')
    area_t = input1.variables['area_t'][:]
    print 'area_t at 1000,100=\n ',area_t[1000,1000] 
    #input1.close()

    print 'Reading file' + data_file
    input2 = Dataset(data_file, 'r')
    rho = input2.variables['pot_rho_0'][:]
    wt = input2.variables['wt'][:]
    dzt = input2.variables['dzt'][:]
    print 'shape rho=\n ',rho.shape
    #input.close()
    
    #sum w*area per
    km=rho.shape[1]
    jm=rho.shape[2]
    im=rho.shape[3]
    print 'km,jm,im',km,jm,im

    #set land vals to 0
    index=rho.mask
    rho[index]=0
    index=dzt.mask
    dzt[index]=0

    #Define density classes
    #find min and max rho
    inc=1
    print 'inc', inc
    #minval = min(rho[nonzero(rho)]) 
    minval=1020
    print 'min val', minval
    #maxval = max(rho[nonzero(rho)]) 
    maxval=1021
    print 'max val', maxval
    rhobin = arange(minval-inc*2, maxval+inc*2, inc)
    print 'rhobin', rhobin

    #creat optimization array of zeros
    opt=zeros((jm,im))
    
    # Set to zero the transport (ta) and
    # overturning (tb) arrays in depth-rho space
    rm=rhobin.shape[0]
    ta=zeros((km,rm))    
    tb=zeros((km,rm))    

    for k in range(0,km-1):
        print 'k level', k
        for ii in range(0,rhobin.shape[0]-1):
            print 'rhobin ', rhobin[ii]
            s1=0
            #range from 1 to im -1 with 0 start index
            for i in range(1,im-1):
                for j in range(0,jm):
                    #check for land mask here
                    #if ww.mask[j,i]=FALSE??? ...maybe not needed caused zerod
                    ww=wt[0,k,j,i]
                    rr=rho[0,k,j,i]
                    dz=dzt[0,k,j,i]
                    area=area_t[j,i]
                    #print area, dz, ww, rr
                    
                    if rr > rhobin[ii] and rr <= rhobin[ii+1]:
                        #avoid double counting
                        if opt[j,i] < 0.5:    
                            s1=s1+ww*area
                            opt[j,i]=1.
            
            ta[k,ii] = s1*1.e-6   # transport in Sv

    #sum up the transport (ta) to obtain overturning (tb)
    #in depth (depth) and density (rhobin) space
    for k in range(0,km):
        for ii in range(1,rhobin.shape[0]):
            tb[k,ii] = tb[k,ii-1] + ta[k,ii]


    output_file = 'rho_z_moc_ps_sig0.nc'
    print "Writing output file ",output_file
    # Output to NetCDF file
    output = Dataset(output_file, 'w', format='NETCDF4')

    output.createDimension('st_ocean', km)
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

    
    mx_var = output.createVariable('rho_z_trans', 'f8', ('time', 'latitude', 'longitude',))
    mx_var[0,:,:] = tb
    mx_var.units = 'Sv'

    print 'finished \n'


    #if __name__ == "__main":
    #    rhozmoc(data_file,grid_file)
        
     

   



