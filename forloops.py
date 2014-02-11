import numpy as np
import glob
import test
from matplotlib import pyplot

fdata='/Users/johnspence/Documents/CarpentryBootcamp/teaching/swc-python/novice/'

fname=fdata+'inflammation-01.csv'

data=np.loadtxt(fname, delimiter=',')

a=np.random.rand(3,2)

#range creates a list not an array
a=range(0,100,5)

#np creates arrays
a=np.arange(0,100,5)

def average(array):
    assert array.size>0, 'At least 1 value required'
    #return array.mean()
    sum=0.0
    for n in range(array.size):
        print 'n index: ',  n, 'array val: ', a[n]
        sum+=array[n]
    if sum > 0:
        return sum/array.size
    else:
        return 0

ma=average(a)
print 'mean array: ', ma


def average2(array):
    #return array.mean()
    sum=0.0
    cnt=0
    for n in array:
        print 'n index: ',  cnt, 'array val: ', n
        sum+=n
        cnt=cnt+1
    if sum > 0:
        return sum/array.size
    else:
        return 0

ma=average2(a)
print 'mean2 array: ', ma

#for loops work as lists - cycles thru number of elements in list

fglob=fdata+'*.csv'
print glob.glob(fglob)
filenames=glob.glob(fglob)
filenames=filenames[0:3]

