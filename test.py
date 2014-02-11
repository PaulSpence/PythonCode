import numpy as np
import glob

from matplotlib import pyplot

fdata='teaching/swc-python/novice/inflammation-01.csv'

data=np.loadtxt(fname='teaching/swc-python/novice/inflammation-01.csv', delimiter=',')
print data
print data[0:4, 1]

print type(data)

print data.shape

print 'first value in data:', data[0, 0]
print 'almost middle value in data:', data[30, 20]

print data[0:4, 0:10]

print data[0:10:3, 0:10:2]


print data.mean()

print 'maximum inflammation:', data.max()
print 'minimum inflammation:', data.min()
print 'standard deviation:', data.std()


patient_0 = data[0, :] # 0 on the first axis, everything on the second
print 'maximum inflammation for patient 0:', patient_0.max()

print data.mean(axis=0)

pyplot.imshow(data)
pyplot.show()

def fahr_to_kelvin(temp):
    return ((temp-32.0)*5.0/9.0+273+.15)

print 'freezing point of water', fahr_to_kelvin(32)
print 'boiling point of water', fahr_to_kelvin(212)


def fahr_to_kelvin_2(temp):
    return ((temp-32)*5/9+273+.15)

print 'freezing point of water 2', fahr_to_kelvin_2(32)
print 'boiling point of water 2', fahr_to_kelvin_2(212)

def kelvin_to_celsius(temp):
    return (temp-273.15)


def fahr_to_celsius(temp):
    temp_k = fahr_to_kelvin(temp)
    result = kelvin_to_celsius(temp_k)
    return result

print 'freezing point of water in Celsius:', fahr_to_celsius(32.0)

def fence(original,wrapper):
    return wrapper+original+wrapper

print 'fence string: ', fence('paul','kial')


def outer(original):
    return original[0]+original[-1]

print 'original string: ', outer('helium')

def centre(data,desired):
    'Return a new array containing the original data centered around the desired value.'
    return (data-data.mean()) +desired

#help(centre)

z=np.zeros((2,2))

z=centre(z,3)

print z

def span(a):
    'max -min of data'
    diff = a.max() - a.min()
    return diff

print 'span of data', span(data)

print 'original min, mean, and max are:', data.min(), data.mean(), data.max()
centered = centre(data, 0)
print 'min, mean, and and max of centered data are:', centered.min(), centered.mean(), centered.max()

print 'std dev before and after:', data.std(), centered.std()

print outer(fence('carbon', '+'))

def analyze(fname):
    ave = data.mean(axis=0)
    pyplot.plot(ave)
    pyplot.show()

    pyplot.plot(data.max(axis=0))
    pyplot.show()

    print 'minimum inflammation per day'
    pyplot.plot(data.min(axis=0))
    pyplot.show()

analyze(fdata)

def rescale(a):
    result=(a[:]-a.max())/(a.max()-a.min())
    return result

a=np.random.rand(3,2)
#start (0default), stop, step
#aa=range(0,100,5)

b=rescale(a)

print 'rescale rand', a


#for loops
def print_characters(element):
    for char in elelment:
        print char
    



