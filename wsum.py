#!/usr/bin/env python
from netCDF4 import *
import numpy as np

#dir(x)
#reload_ext autoreload
#autoreload
#who
#dir()
#whos

def wsum (data_file='f',grid_file='f'):

   
    #tx_trans = input.variables['tx_trans'][0,:,:,:]
    #mass_transport[n-min,:,:] = sum(tx_trans, axis=0)
    
    data_file = '/g/data1/v45/APE-MOM/gfdl_nyf_1080_cp/ocean_541-550.nc'
    grid_file = '/short/v45/pas561/mom/archive/ocean_grid.nc'
     
    print 'Reading file ' + grid_file
    input1 = Dataset(grid_file, 'r')
    area_t = input1.variables['area_t'][:]
    ht = input1.variables['ht'][:]
    geolat_t = input1.variables['geolat_t'][:]
    geolon_t = input1.variables['geolon_t'][:]
    print 'area_t at 1000,100=\n ',area_t[1000,1000] 
    input1.close()

    print 'Reading file' + data_file
    input2 = Dataset(data_file, 'r')
    sw_ocean = input2.variables['sw_ocean'][:]
    wt = input2.variables['wt'][:]
    rho2 = input2.variables['pot_rho_2'][:]
    print 'shape w=\n ',wt.shape
    print 'shape rho2=\n ',rho2.shape
    print 'wt at 100,100,100=\n ',wt[0,1,1000,1000] 
    input2.close()
    print 'shape w=\n ',wt.shape
    
    km=wt.shape[1]
    jm=wt.shape[2]
    im=wt.shape[3]
    print 'km,jm,im',km,jm,im

    index=wt.mask
    wt[index]=0
    index=rho2.mask
    rho2[index]=0
    index=ht.mask
    ht[index]=0
 
    rhomin=1037.05  
    htmin =0.   
    latmax=-65. 
    lonmin=-62.
    lonmax=0.

    #create mask for Weddell Sea
    #condition=N.logical_and(geolon_t>=lonmin, geolon_t<=lonmax, geolat_t<=latmax, ht>htmin)
    #wedwt=N.where(condition,wt,0)

    wedint=np.zeros(km)
    for k in xrange(km):
        for j in xrange(jm):
            for i in xrange(im):
                if rho2.data[0,k,j,i]>rhomin and ht[j,i]>htmin  and geolon_t[j,i]>=lonmin \
                    and geolon_t[j,i]<=lonmax and geolat_t[j,i]<=latmax:
                    wedint[k] = wedint[k] + wt.data[0,k,j,i]*area_t[j,i]
                else:
                    pass
   
    for k in xrange(km):
        print 'wsum at k \n',wedint[k],k

    
    print 'finished \n'

        
     

   



