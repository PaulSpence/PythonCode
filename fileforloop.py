"""
Write purpose
"""

import pdb
import numpy as np
import netCDF4 as nc4

import glob
import os
import logging


basepath = '../gfdl_nyf_1080/output*'

def slurp(path, vname):
    """ Read a variable while closing the file immediately
    """
    ifile = nc4.Dataset(path)
    var = ifile.variables[vname][:]
    ifile.close()
    return var
    
geolat_c = slurp('../gfdl_nyf_1080/output101/ocean_grid.nc','geolat_c')
geolon_c = slurp('../gfdl_nyf_1080/output101/ocean_grid.nc','geolat_c')
tx_trans = slurp('../gfdl_nyf_1080/output101/ocean.nc','tx_trans')
sw_ocean = slurp('../gfdl_nyf_1080/output101/ocean.nc','sw_ocean')

runs = sorted(glob.glob(basepath))
pdb.set_trace()




for path in runs[20:]: #will process runs 20 forward

    tx_trans = slurp(os.path.join(path,'ocean.nc'), 'tx_trans')

    
