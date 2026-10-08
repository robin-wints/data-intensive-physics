# cpu_bound_task.py
import sys
import time
import threading
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
    
    
def main(iterations,num_threads):
    results = [0]*num_threads
    calculations_per_thread = int(iterations//num_threads)
    remainder = int(iterations%num_threads)
    itperthread = []
    for i in range(num_threads):
        itperthread.append(calculations_per_thread)
        if i<remainder:
            itperthread[i] += 1
    threads = []

    start_time = time.time()
    istart = 0
    iend = 0
    for j in range(num_threads):
        istart = iend
        iend += itperthread[j]
        thread = threading.Thread(target=heavy_calculation, args=(iterations,results,j,istart,iend))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Pi = {sum(results)*4/iterations:} Iterations: {iterations:d} Execution time: {end_time - start_time:9.7f} seconds, {num_threads} threads")

if __name__ == "__main__":
    if int(len(sys.argv)) == 3: # total number of arguments to python
        iterations = int(sys.argv[1])
        threads = int(sys.argv[2])
        result = main(iterations,threads)
    else:
        print("Usage: python {} <ITERATIONS> <THREADS>".format(sys.argv[0]))

