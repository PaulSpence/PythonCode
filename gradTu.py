from netCDF4 import *
import numpy as np


# Grad(Tu)

def gradTu (grid_file):

    grid_file = '/short/v45/pas561/mom/archive/gfdl_nyf_1080/ocean_grid.nc'
     
    print 'Reading file ' + grid_file
    input1 = Dataset(grid_file, 'r')
    area_t = input1.variables['area_t'][:]
    area_u = input1.variables['area_u'][:]
    geolon_t = input1.variables['geolon_t'][:]
    geolat_t = input1.variables['geolat_t'][:]
    geolon_c = input1.variables['geolon_c'][:]
    geolat_c = input1.variables['geolat_c'][:]
    yt_ocean = input1.variables['yt_ocean'][:]
    xt_ocean = input1.variables['xt_ocean'][:]
    yu_ocean = input1.variables['yu_ocean'][:]
    xu_ocean = input1.variables['xu_ocean'][:]
    ht = input1.variables['ht'][:]
    #dxt = input1.variables['dxt'][:]
    #dyt = input1.variables['dxt'][:]
    #dxu = input1.variables['dxu'][:]
    #dyu = input1.variables['dyu'][:]
    input1.close()

    #calc gradTpUc
    data_file='/short/v45/pas561/mom/archive/gfdl_nyf_1080_PI_Ant_20Eto140E/5yrs_5day/check/temp.IC200.5day.cat.diff.yr3jan.nc'  
    
    print 'Reading file ' + data_file
    input1 = Dataset(data_file, 'r')
    temp = input1.variables['temp'][:]
    input1.close()

    data_file='/short/v45/pas561/mom/archive/gfdl_nyf_1080_cp/5yrs_5day/check/u.IC200.5day.cat.yr3jan.nc'  
    
    print 'Reading file ' + data_file
    input1 = Dataset(data_file, 'r')
    u = input1.variables['u'][:]
    input1.close()

    data_file='/short/v45/pas561/mom/archive/gfdl_nyf_1080_cp/5yrs_5day/check/dzt.IC200.5day.cat.yr3jan.nc'  
    
    print 'Reading file ' + data_file
    input1 = Dataset(data_file, 'r')
    dzt = input1.variables['dzt'][:]
    input1.close()
    
    #note that temp and dzt have different km shape(12 instead of 10)
    tm=u.shape[0]
    km=u.shape[1]
    jm=u.shape[2]
    im=u.shape[3]
    print 'tm,km,jm,im',tm,km,jm,im

    #create land/sea masks
    temp_3d = temp[0,:,:,:]
    tmsk = np.ones(np.shape(temp_3d))
    index = temp_3d.mask
    tmsk[index] = 0

    #set land vals to 0
    index=temp.mask
    temp[index]=0
    index=dzt.mask
    dzt[index]=0
    index=u.mask
    u[index]=0
    
    #interp Temp onto Vel grid
    Tvg=np.zeros((jm,im))
    for t in range(tm):
        for k in range(km):
            for j in range(jm):
                for i in range(im):
                    #Tvg(t,k,j,i)=
                    t=1
                    t=1
                    t=1
                    t=1    



    advx_TpUc=np.zeros((jm,im))

    #start with 1 grid cell: 2,100,1000
    for t in range(tm):
        #for j in range(1,jm-2):
        for j in range(99,100):
            for k in range(1,2):
                for i in range(999,1000):
                    print 't,j,k,i temp[t,1,99,999] ', t,k,j,i,temp[t,k,j,i]
                    #dlon=np.abs(geolon_t[j,i+1]-geolon_t[j,i])
                    #dxt[j,i]= r*np.cos(geolat_t[j,i]*np.pi/180)*dlon*np.pi/180
        
        #dxt[j,im-1]=dxt[j,im-2]

    #output_file = 'dxtdyt.nc'
    #print "Writing output file ",output_file
    # Output to NetCDF file
    #output = Dataset(output_file, 'w', format='NETCDF4')

    #output.createDimension('yt_ocean', jm)
    #y_var = output.createVariable('yt_ocean', 'f8', ('yt_ocean',))
    #y_var.units = 'meters'
    #y_var[:] = yt_ocean[:]

    #output.createDimension('xt_ocean', im)
    #x_var = output.createVariable('xt_ocean', 'f8', ('xt_ocean',))
    #x_var.units = 'meters'
    #x_var[:] = xt_ocean[:]

    #dx_var = output.createVariable('dxt', 'f8', ('yt_ocean', 'xt_ocean',))
    #dx_var.units = 'm'
    #dx_var[:,:] = dxt
    
    #output.close()


    
    print 'finished \n'

    if __name__ == "__main":
        areadxtdyt(data_file,grid_file)
        
     

   



