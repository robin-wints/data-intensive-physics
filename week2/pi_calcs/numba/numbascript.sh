#!/bin/bash
# ======================
# numbascript.sh
# ======================
#SBATCH --job-name=test_job
#SBATCH --partition=teach_cpu
#SBATCH --account=phys040684
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=24
#SBATCH --time=0:10:0
#SBATCH --mem=200M

# Load modules required for runtime either the module way:
# module add languages / python
# Or the Mamba way :
source ~/data-intensive-physics/initMamba.sh
mamba activate dip

# Changes directory to the one being looked at when the 
# job was submitted.
cd $SLURM_SUBMIT_DIR
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}

# Now run your program with the usual command
python picalc_numba.py 10000000
python picalc_numba1.py 10000000