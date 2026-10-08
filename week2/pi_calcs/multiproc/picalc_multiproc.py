# cpu_bound_task.py
import sys
import os
import csv
import time
import multiprocessing
from math import sqrt

def heavy_calculation(nmax,results,slice,istart,iend):
    """A function that simulates a CPU-bound task."""
    dx = 1.0 / nmax
    pibyfour = 0.0
    for i in range(istart,iend):
        idx = i*dx
        pibyfour += sqrt(1-idx*idx)
    results[slice] = pibyfour
    
    
def main(iterations,num_procs,filename):
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

    pi = sum(results)*4/iterations

    end_time = time.time()
    ex_time = end_time-start_time 

    exists =  os.path.isfile(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow(['n_procs', 'pi', 'time'])
        
        writer.writerow([num_procs, pi, ex_time])

    print(f"Pi = {pi:} Iterations: {iterations:d} Execution time: {ex_time:9.7f} seconds, {num_procs} procs")

if __name__ == "__main__":
    if int(len(sys.argv)) == 3: # total number of arguments to python
        iterations = int(sys.argv[1])
        procs = int(sys.argv[2])
        filename = './info.csv'
        result = main(iterations,procs,filename)
    elif int(len(sys.argv)) == 4: # total number of arguments to python
        iterations = int(sys.argv[1])
        procs = int(sys.argv[2])
        filename = sys.argv[3]
        result = main(iterations,procs,filename)
    else:
        print("Usage: python {} <ITERATIONS> <NUMPROCS> <FILENAME>".format(sys.argv[0]))

