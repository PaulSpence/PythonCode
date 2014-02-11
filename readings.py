import sys
import numpy as np

def main():
    script = sys.argv[0]
    filename = sys.argv[1]
    data = np.loadtxt(filename,delimiter=',')
    
    #loop over every patient in file 
    for m in data.mean(axis=1):
        print m

main()
