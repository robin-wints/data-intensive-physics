# cpu_bound_task.py
import sys
import time
import multiprocessing
#import numpy as np
from math import sqrt

def heavy_calculation(nmax,results,slice,istart,iend):
    """A function that simulates a CPU-bound task."""
    dx = 1.0 / nmax
    pibyfour = 0.0
    for i in range(istart,iend):
        idx = i*dx
        pibyfour += sqrt(1-idx*idx)
    results[slice] = pibyfour
    
    
def main(iterations,num_procs):
    results = multiprocessing.Array('d',range(num_procs))
    calculations_per_proc = int(iterations//num_procs)
    remainder = int(iterations%num_procs)
    itperproc = []
    for i in range(num_procs):
        itperproc.append(calculations_per_proc)
        if i<remainder:
            itperproc[i] += 1
    procs = []

    start_time = time.time()
    istart = 0
    iend = 0
    for j in range(num_procs):
        istart = iend
        iend += itperproc[j]
        proc = multiprocessing.Process(target=heavy_calculation, args=(iterations,results,j,istart,iend))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    end_time = time.time()
    print(f"Pi = {sum(results)*4/iterations:} Iterations: {iterations:d} Execution time: {end_time - start_time:9.7f} seconds, {num_procs} procs")

if __name__ == "__main__":
    if int(len(sys.argv)) == 3: # total number of arguments to python
        iterations = int(sys.argv[1])
        procs = int(sys.argv[2])
        result = main(iterations,procs)
    else:
        print("Usage: python {} <ITERATIONS> <NUMPROCS>".format(sys.argv[0]))

