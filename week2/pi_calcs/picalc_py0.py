import sys
import time
from numpy import sqrt

def main( nmax ):
    pibyfour = 0.0
    dx = 1.0 / nmax
    
    for i in range(nmax):
        pibyfour += sqrt(1-pow((i*dx),2))
    
    pi = 4.0 * pibyfour * dx
    return pi

if __name__ == '__main__':
    if int(len(sys.argv)) == 2:
        nmax = int(sys.argv[1])
        initial = time.time()
        pi = main(nmax)
        final = time.time()
        print("Pi = {:18.16f}".format(pi))
        print("Iterations: {:d} Elapsed time: {:9.7f} s".format(nmax,final-initial))
    else:
        print("Usage: python {} <ITERATIONS>".format(sys.argv[0]))
