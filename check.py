import sys
import numpy as np
import glob

def main():
    script = sys.argv[0]
    flag = sys.argv[1]

    for f in sys.argv[2:]:
        print f
        val = process(f,flag)
        print val
        print type(val)
        for m in [val]:
            print val

def process(fname,flag):
    data=np.loadtxt(fname, delimiter=',')
    print data.shape
        
    assert flag in ['--min', '--max', '--mean'], \
    """Flag is not valid"""

    if flag=='--min':
        values = data.min()
    elif flag=='--max':
        values = data.max()
    elif flag == '--mean': 
        values = data.mean()
    
    return values

main()
