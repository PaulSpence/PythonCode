from netCDF4 import *
import numpy as np


# Grad(Tu)

def areadxtdyt (grid_file):

    grid_file = '/short/v45/pas561/mom/archive/gfdl_nyf_1080/output201/ocean_grid.nc'
     
    print 'Reading file ' + grid_file
    input1 = Dataset(grid_file, 'r')
    area_t = input1.variables['area_t'][:]
    print 'area_t at 1000,100=\n ',area_t[1000,1000] 
    area_u = input1.variables['area_u'][:]

    geolon_t = input1.variables['geolon_t'][:]
    geolat_t = input1.variables['geolat_t'][:]
    geolon_c = input1.variables['geolon_c'][:]
    geolat_c = input1.variables['geolat_c'][:]
    yt_ocean = input1.variables['yt_ocean'][:]
    xt_ocean = input1.variables['xt_ocean'][:]
    yu_ocean = input1.variables['yu_ocean'][:]
    xu_ocean = input1.variables['xu_ocean'][:]
    
    input1.close()

    jm=area_t.shape[0]
    im=area_t.shape[1]
    print 'jm,im',jm,im
    print 'shape area_t=\n ',area_t.shape
    
    r=6378000
    dxt=np.zeros((jm,im))
    dyt=np.zeros((jm,im))
    a=np.zeros((jm,im))
    print 'shape a=\n ',a.shape

    for j in range(jm):
        #print 'j', j
        for i in range(im-1):
            dlon=np.abs(geolon_t[j,i+1]-geolon_t[j,i])
            dxt[j,i]= r*np.cos(geolat_t[j,i]*np.pi/180)*dlon*np.pi/180
        
        dxt[j,im-1]=dxt[j,im-2]

    for i in range(im):
        for j in range(jm-1):
            dlat=np.abs(geolat_t[j+1,i]-geolat_t[j,i])
            dyt[j,i]= r*dlat*np.pi/180
        
        dyt[jm-1,i]=dyt[jm-2,i]

    for j in range(jm):
        for i in range(im):
            a[j,i]=dxt[j,i]*dyt[j,i]
 
    print 'a[100,100] sum',a[100,100],np.sum(a)
    print 'area_t[100,100]',area_t[100,100],np.sum(area_t)

    jm=area_t.shape[0]
    im=area_t.shape[1]
    print 'jm,im',jm,im
    print 'shape area_t=\n ',area_t.shape

    r=6378000
    dxc=np.zeros((jm,im))
    dyc=np.zeros((jm,im))
    ac=np.zeros((jm,im))
    print 'shape ac=\n ',ac.shape

    for j in range(jm):
        #print 'j', j
        for i in range(im-1):
            dlon=np.abs(geolon_c[j,i+1]-geolon_c[j,i])
            dxc[j,i]= r*np.cos(geolat_c[j,i]*np.pi/180)*dlon*np.pi/180
        
        dxc[j,im-1]=dxc[j,im-2]

    for i in range(im):
        for j in range(jm-1):
            dlat=np.abs(geolat_c[j+1,i]-geolat_c[j,i])
            dyc[j,i]= r*dlat*np.pi/180
        
        dyc[jm-1,i]=dyc[jm-2,i]

    for j in range(jm):
        for i in range(im):
            ac[j,i]=dxc[j,i]*dyc[j,i]
 
    print 'a[100,100] sum',ac[100,100],np.sum(ac)
    print 'area_t[100,100]',area_u[100,100],np.sum(area_u)

    output_file = 'dxtdyt.nc'
    print "Writing output file ",output_file
    # Output to NetCDF file
    output = Dataset(output_file, 'w', format='NETCDF4')

    output.createDimension('yt_ocean', jm)
    y_var = output.createVariable('yt_ocean', 'f8', ('yt_ocean',))
    y_var.units = 'meters'
    y_var[:] = yt_ocean[:]

    output.createDimension('xt_ocean', im)
    x_var = output.createVariable('xt_ocean', 'f8', ('xt_ocean',))
    x_var.units = 'meters'
    x_var[:] = xt_ocean[:]

    output.createDimension('yu_ocean', jm)
    yu_var = output.createVariable('yu_ocean', 'f8', ('yu_ocean',))
    yu_var.units = 'meters'
    yu_var[:] = yu_ocean[:]

    output.createDimension('xu_ocean', im)
    xu_var = output.createVariable('xu_ocean', 'f8', ('xu_ocean',))
    xu_var.units = 'meters'
    xu_var[:] = xu_ocean[:]

    dx_var = output.createVariable('dxt', 'f8', ('yt_ocean', 'xt_ocean',))
    dx_var.units = 'm'
    dx_var[:,:] = dxt


    dy_var = output.createVariable('dyt', 'f8', ('yt_ocean', 'xt_ocean',))
    dy_var.units = 'm'
    dy_var[:,:] = dyt

    a_var = output.createVariable('dyt*dxt', 'f8', ('yt_ocean', 'xt_ocean',))
    a_var.units = 'm2'
    a_var[:,:] = a


    dxc_var = output.createVariable('dxu', 'f8', ('yu_ocean', 'xu_ocean',))
    dxc_var.units = 'm'
    dxc_var[:,:] = dxc


    dyc_var = output.createVariable('dyu', 'f8', ('yu_ocean', 'xu_ocean',))
    dyc_var.units = 'm'
    dyc_var[:,:] = dyc

    ac_var = output.createVariable('dyu*dxu', 'f8', ('yu_ocean', 'xu_ocean',))
    ac_var.units = 'm2'
    ac_var[:,:] = ac



    output.close()


    
    print 'finished \n'

    if __name__ == "__main":
        areadxtdyt(data_file,grid_file)
        
     

   



