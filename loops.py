import numpy as np
import glob
import test
from matplotlib import pyplot

fdata='/Users/johnspence/Documents/CarpentryBootcamp/teaching/swc-python/novice/'

fname=fdata+'inflammation-01.csv'

data=np.loadtxt(fname, delimiter=',')


#for loops
def print_characters(element):
    for char in element:
        print char

print_characters(fdata)


def rescale(a):
    result=(a[:]-a.max())/(a.max()-a.min())
    return result

a=np.random.rand(3,2)

#range creates a list not an array
a=range(0,100,5)

#np creates arrays
a=np.arange(0,100,5)

b=rescale(a)


odds=[1,3,4,5]
type(odds)
odds[-1]

#show attributes
dir(odds)

def sign(num):
    if num > 0:
        return 1
    elif num == 0:
        return 0
    else:
        return -1

print 'sign of -3:', sign(-3)

if (1 > 0) and (-1 > 0):
    print 'both parts are true'
else:
    print 'one part is not true'

if (1 < 0) or ('left' < 'right'):
    print 'at least one test is true'

def near(first,second):
    value=(first*1.0)/(second*1.0)
    if (value >= .9) and (value <= 1.1):
        return 'TRUE'
    else:
        return 'FALSE'

data=np.loadtxt(fname, delimiter=',')
width, height = data.shape
heatmap=data

for x in range(width):
    for y in range(height):
        if data[x,y] < data.mean():
            heatmap[x,y] = -1
        elif data[x,y] == data.mean():
            heatmap[x,y] = 0
        else:
            heatmap[x,y] = 1
       
pyplot.imshow(heatmap)
pyplot.show()

numbers = [1.5, 2.3, 0.7, 0.001, 4.4]
total = 0.0

for n in numbers:
    assert n>=0.0, 'Data should only contain +ve values'
    total += n

print 'total is:', total

def normalize_rectangle(rect):
    assert len(rect) == 4, 'Rectangles must contain 4 coordinates'
    x0, y0, x1, y1 = rect
    assert x0 < x1, 'Invalid X coordinates'
    assert y0 < y1, 'Invalid Y coordinates'

    dx = x1 - x0
    dy = y1 - y0
    if dx > dy:
        scaled = float(dy) / dx
        upper_x, upper_y = 1.0, scaled
    else:
        scaled = float(dx) / dy
        upper_x, upper_y = scaled, 1.0

    assert 0 < upper_x <= 1.0, 'Calculated upper X coordinate invalid'
    assert 0 < upper_y <= 1.0, 'Calculated upper Y coordinate invalid'

    return (0, 0, upper_x, upper_y)


#print normalize_rectangle( (4.0, 2.0, 1.0, 5.0) )
print normalize_rectangle( (0.0, 0.0, 1.0, 5.0) )

def average(array):
    assert array.size>0, 'At least 1 value required'
    #return array.mean()
    sum=0.0
    for n in array:
        print 'n index: ',  n
        sum+=n
    if sum > 0:
        return sum/array.size
    else:
        return 0

#for loops work as lists - cycles thru number of elements in list

fglob=fdata+'*.csv'
print glob.glob(fglob)
filenames=glob.glob(fglob)
filenames=filenames[0:3]

filenames = filenames[0:3]
for f in filenames:
    print f
    test.analyze(f)
