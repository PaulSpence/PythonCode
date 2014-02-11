import numpy as np
import netCDF4 as nc
import os
import pylab as pylab
from scipy import stats
# run the script by doing:
#   1- python script_name
#   2- run script name



 
file_name='slp.1979to2007.nc'
#file_name='t_10.1979.05APR2010.nc'
var_name='SLP'

file_out = 'trends_slp.1979to2007.nc'
#file_out = 'trends_T_10_1979.nc'
os.system('rm '+file_out )

# LOAD FILE
fin=nc.Dataset(file_name)

# READ VARIABLE
T=fin.variables[var_name][:]# print values: print T[:]
LAT=fin.variables['LAT'][:]# print values: print T[:]
LON=fin.variables['LON'][:]# print values: print T[:]

# READ VARIABLES ATTRIBUTES
varatt={}
for attname in fin.variables[var_name].ncattrs():
	varatt[attname]=getattr(fin.variables[var_name], attname)

# READ GLOBAL ATTRIBUTES
globatt={}
for attname in fin.ncattrs():
	globatt[attname]=getattr(fin, attname)


fin.close()


# START ANALYSIS

tt=np.arange(1,T.shape[0]+1)
print T.shape

slopev=np.zeros((T.shape[1],T.shape[2]))
interceptv=np.zeros((T.shape[1],T.shape[2]))
r_valuev=np.zeros((T.shape[1],T.shape[2]))
p_valuev=np.zeros((T.shape[1],T.shape[2]))
std_errv=np.zeros((T.shape[1],T.shape[2]))


for ii in np.arange(0,T.shape[1]):
	print 'latitude', ii
	for jj in np.arange(0,T.shape[2]):
		#print 'longitude', jj
		#m,b = pylab.ployfit(x,T[:,ii,jj],1)
		slope, intercept, r_value, p_value, std_err = stats.linregress(tt,T[:,ii,jj])		
		slopev[ii,jj]=slope
		interceptv[ii,jj]=intercept
		r_valuev[ii,jj]=r_value
		p_valuev[ii,jj]=p_value
		std_errv[ii,jj]=std_err


netcdf_files=True
# ############################################################################
# CREATING NETCDF FILE
if netcdf_files==True:

	# Create output file
	print '****************************************************************************'
	print 'Output is in ', file_out
	print '****************************************************************************'
	fout=nc.Dataset(file_out,mode='w', format='NETCDF3_CLASSIC')

	# Create dimensions     
	fout.createDimension('lat', slopev.shape[0])
	fout.createDimension('lon', slopev.shape[1])

	# Create variables
	outvar=fout.createVariable('slope', 'f8',['lat','lon'])
	outvar[:]=slopev

	lon=fout.createVariable('LON', 'f8',['lon'])
	lon[:]=LON

	lat=fout.createVariable('LAT', 'f8',['lat'])
	lat[:]=LAT


	outvar2=fout.createVariable('intercept', 'f8',['lat','lon'])
	outvar2[:]=interceptv
	
	outvar3=fout.createVariable('p_value', 'f8',['lat','lon'])
	outvar3[:]=p_valuev

	outvar4=fout.createVariable('r_value', 'f8',['lat','lon'])
	outvar4[:]=r_valuev
	
	# Copy attributes from invar and create some new ones:
	for attname in varatt.keys():
		if attname!='_FillValue':
			setattr(outvar,attname,varatt[attname])

	# Add global attributes
	for attname in globatt.keys():
		setattr(fout,attname,globatt[attname])

	fout.close()

