import sys
import time
from math import sqrt

def main( nmax ):

    pibyfour = 0.0
    dx = 1.0 / nmax
    
    initial = time.time()
    
    for i in range(nmax):
        idx = i*dx
        pibyfour += sqrt(1-idx*idx)
    
    final = time.time()
    
    print("Iterations: {:d} Elapsed time: {:9.7f} s".format(nmax, final-initial))

    pi = 4.0 * pibyfour * dx
    print("Pi = {:18.16f}".format(pi))
    
    return 0

if __name__ == '__main__':
    if int(len(sys.argv)) == 2:
        main(int(sys.argv[1]))
    else:
        print("Usage: python {} <ITERATIONS>".format(sys.argv[0]))
