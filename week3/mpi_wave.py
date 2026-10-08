#***************************************************************************
# FILE: mpi_wave.py
# DESCRIPTION:
#   MPI Concurrent Wave Equation - Python Version
#   Point-to-Point Communications Example
#   This program implements the concurrent wave equation described
#   in Chapter 5 of Fox et al., 1988, Solving Problems on Concurrent
#   Processors, vol 1.  NB this is a standing wave!
#   A vibrating string is decomposed into points.  Each processor is
#   responsible for updating the amplitude of a number of points over
#   time. At each iteration, each processor exchanges boundary points with
#   nearest neighbors.  This version uses low level sends and receives
#   to exchange boundary points.
# AUTHOR: Blaise Barney. Adapted from Ros Leibensperger, Cornell Theory
#    Center. Converted to MPI: George L. Gusciora, MHPCC (1/95)
# LAST REVISED: 07/05/05.  Converted to Python / mpi4py SH (27/10/18)
#***************************************************************************
from mpi4py import MPI
import os
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
import matplotlib.pyplot as plt

MASTER = 0
TPOINTS = 800
MAXSTEPS = 10000
RtoL = 10
LtoR = 20
OUT1 = 30
OUT2 = 40

nsteps = 0
npoints = 0
first = 0
values = np.zeros(TPOINTS+2,dtype=np.float64)  # values at time t
oldval = np.zeros(TPOINTS+2,dtype=np.float64)  # values at time (t-dt)
newval = np.zeros(TPOINTS+2,dtype=np.float64)  # values at time (t+dt)
#**************************** functions ************************************
def init_master():
    """
    Master obtains timestep input value from user and broadcasts it
    """
#
# Set number of number of time steps and then print and broadcast
#
    global nsteps
    while ((nsteps < 1) or (nsteps > MAXSTEPS)):
        tchar = input("Enter number of time steps (1-%d): " % MAXSTEPS)
        nsteps = int(tchar)
    nsteps = comm.bcast(nsteps, root=MASTER)

#***************************************************************************
def init_workers():
    """
    Workers receive timestep input value from master
    """
    global nsteps
    nsteps = comm.bcast(nsteps, root=MASTER)

#***************************************************************************
def init_line():
    """
    All processes initialize points on line
    """
#
# calculate initial values based on sine curve */
#
    global npoints, first
    nmin = int(TPOINTS/numtasks)
    nleft = TPOINTS%numtasks
    fac = 2.0 * np.pi
    k = 0
    for i in range(numtasks):
        if i<nleft:
            npts = nmin+1
        else:
            npts = nmin
        if (taskid == i):
            first = k + 1
            npoints = npts
            print ("task=%3d  first point=%5d  npoints=%4d" % (taskid,first,npts))
            for j in range(1,npts+1):
                k += 1
                x = k/(TPOINTS - 1)
                values[j] = np.sin (fac * x)
        else:
            k += npts;
    for i in range (1,npoints+1):
        oldval[i] = values[i]

#***************************************************************************
def update(left, right):
    """
    All processes update their points a specified number of times
    """
    dtime = 0.3
    c = 1.0
    dx = 1.0
    tau = (c * dtime / dx)
    sqtau = tau * tau
#
# Update values for each point along string
#
    for i in range(1,nsteps+1):
#
        if (first != 1):  # Exchange data with "left-hand" neighbor
            comm.Send(values[1], dest=left, tag=RtoL)
            comm.Recv([values[0:],1,MPI.DOUBLE], source=left, tag=LtoR)
#
        if (first + npoints -1 != TPOINTS):  # Exchange data with "right-hand" neighbor
            comm.Send(values[npoints], dest=right, tag=LtoR)
            comm.Recv([values[npoints+1:],1,MPI.DOUBLE], source=right, tag=RtoL)
#
        for j in range(1,npoints+1):  # Update points along line
            if ((first + j - 1 == 1) or (first + j - 1 == TPOINTS)):  # Global endpoints
                newval[j] = 0.0
            else:  # Use wave equation to update points */
                newval[j] = (2.0 * values[j]) - oldval[j] + (sqtau * (values[j-1] - (2.0 * values[j]) + values[j+1]))
#
        for j in range(1,npoints+1):
            oldval[j] = values[j]
            values[j] = newval[j]
#***************************************************************************
def output_master():
    """
    Master receives results from workers and prints
    """
    results = np.zeros(TPOINTS,dtype=np.float64)  # result array
#
# Store worker's results in results array
#
    for i in range(1,numtasks):
        buffer = comm.recv(source=i, tag=OUT1)
        start = buffer[0]
        npts = buffer[1]
        comm.Recv([results[start-1:],npts,MPI.DOUBLE], source=i, tag=OUT2)
#
# Store master's results in results array
#
    for i in range(first,first + npoints):
        results[i-1] = values[i]

    j = 0;
    print("***************************************************************")
    print("Final amplitude values for all points after %d steps:"%nsteps)
    for i in range(0,TPOINTS,10):
        fmlist = ['{:6.2f}' for item in results[i:i+10]]
        s = ''.join(fmlist)
        print(s.format(*results[i:i+10]))
    print("***************************************************************")
#
# display results with matplotlib
#
    print("Drawing graph...")
    print("Click the CLOSE window button or use CTRL-C to quit")
    plt.plot(results)
    plt.show()
#***************************************************************************
def output_workers():
    """
    Workers send the updated values to the master
    """
#
# Send first point, number of points and results to master
#
    buffer = [first,npoints]
    comm.send(buffer, dest=MASTER, tag=OUT1)
    comm.Send([values[1:],npoints,MPI.DOUBLE], dest=MASTER, tag=OUT2)
#***************************** Main program **************************************
#
# Initialisations
#
comm = MPI.COMM_WORLD
numtasks = comm.Get_size()
taskid = comm.Get_rank()

if (numtasks < 2):
    print("ERROR: Number of MPI tasks set to %d" % numtasks)
    print("Need at least 2 tasks!  Quitting...")
    comm.Abort()
#
# Determine left and right neighbors
#
if (taskid == numtasks-1):
    right = 0
else:
    right = taskid + 1

if (taskid == 0):
    left = numtasks - 1
else:
    left = taskid - 1
#
# Get program parameters and initialize wave values
#
if (taskid == MASTER):
    print ("Starting mpi_wave using %d tasks." % numtasks)
    print ("Using %d points on the vibrating string." % TPOINTS)
    init_master()
else:
    init_workers()
init_line()
#
# Update values along the line for nstep time steps
#
update(left, right)
#
# Master collects results from workers and prints
#
if (taskid == MASTER):
    output_master()
else:
    output_workers()
#
#***************************** Main program end **********************************

