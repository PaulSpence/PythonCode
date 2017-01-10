from netCDF4 import *
from numpy import *

import glob
import os

path='/short/v45/pas561/mom/archive/gfdl_nyf_1080_cp/'
all_files=glob.glob(os.path.join(path,'*','*.nc'))

cnt=0
for n in range(len(all_files)):
        print 'nccopy '+ str(n) + ' '+  all_files[n]
	os.system('nccopy -d 5 '+all_files[n] + ' '+ 'tmp.nc')
	os.system('mv '+ 'tmp.nc '+ all_files[n])



