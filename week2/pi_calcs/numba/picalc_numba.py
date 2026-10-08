import sys
from numba import jit
import time
from math import sqrt

@jit(nopython=True)
def main( nmax ):
    pibyfour = 0.0
    dx = 1.0 / nmax
    
    for i in range(nmax):
        idx = i*dx
        pibyfour += sqrt(1-idx*idx)
    
    pi = 4.0 * pibyfour * dx
    return pi

if __name__ == '__main__':
    if int(len(sys.argv)) == 2:
        initial = time.time()
        pi = main(int(sys.argv[1]))
        final = time.time()
        print("Pi = {:18.16f}".format(pi))
        print("Elapsed time: {:8.6f} s".format(final-initial))
    else:
        print("Usage: python {} <ITERATIONS>".format(sys.argv[0]))
