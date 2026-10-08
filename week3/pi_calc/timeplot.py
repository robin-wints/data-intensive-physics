import sys
import pandas as pd
import matplotlib.pyplot as plt

def main(filename):
    info = pd.read_csv(filename)
    
    fig, ax = plt.subplots()
    ax.plot(info['n_tasks'], info['time'])
    ax.set_title('Timings for calculating pi using MPI')
    ax.set_xlabel('Number of MPI Tasks')
    ax.set_ylabel('Time Elapsed (s)')
    fig.savefig('timeplot.png', bbox_inches='tight')

if __name__ == "__main__":
    if int(len(sys.argv)) == 2: # total number of arguments to python
        filename = sys.argv[1]
        result = main(filename)
    else:
        print("Usage: python {} <FILENAME>".format(sys.argv[0]))