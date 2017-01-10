from netCDF4 import *
import numpy as np



def cleanrestarts ():

    #calc gradTpUc
    good='/short/v45/pas561/mom/archive/mom01v5/restart000/ocean_velocity.res.nc'  
    
    print 'Reading file ' + good
    input1 = Dataset(good, 'r')
    u1 = input1.variables['u'][:]
    input1.close()

    bad='/short/v45/pas561/mom/archive/mom01v5/nopartials_restart190/ocean_velocity.res.nc'  
    
    print 'Reading file ' + bad
    input1 = Dataset(bad, 'r')
    u2= input1.variables['u'][:]
    input1.close()

    #note that temp and dzt have different km shape(12 instead of 10)
    tm=u1.shape[0]
    km=u1.shape[1]
    jm=u1.shape[2]
    im=u1.shape[3]
    print 'tm,km,jm,im',tm,km,jm,im

    tm=u2.shape[0]
    km=u2.shape[1]
    jm=u2.shape[2]
    im=u2.shape[3]
    print 'tm,km,jm,im',tm,km,jm,im
    
    #create land/sea masks
    #temp_3d = temp[0,:,:,:]
    tmsk1 = np.ones(np.shape(u1))
    index = u1.mask
    tmsk1[index] = 0

    tmsk2 = np.ones(np.shape(u1))
    index = u2.mask
    tmsk2[index] = 0

    #set land vals to 0
    #index=temp.mask
    #temp[index]=0
    #index=dzt.mask
    #dzt[index]=0
    #index=u.mask
    #u[index]=0
    
    #check land sea mask at surface
    cnt=0
    for t in range(tm):
        for k in range(0):
            print 't,k,', t,k
            #for j in range(jm):
            #    for i in range(im):



                    #print 't,j,k,i temp[t,1,99,999] ', t,k,j,i,temp[t,k,j,i]
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
        cleanrestarts()
        
     

   



