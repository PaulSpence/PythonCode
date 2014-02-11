import sys
import numpy as np
import glob

def main():
    script = sys.argv[0]
    fdir = sys.argv[1]
    ftype = sys.argv[2]
    
    fglob=fdir+ftype
    print glob.glob(fglob)
    
    filenames=glob.glob(fglob)
    filenames=filenames[0:3]

    filenames = filenames[0:3]
    for f in filenames:
        print f


main()
