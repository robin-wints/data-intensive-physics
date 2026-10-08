#!/bin/bash
# ======================
# serialscript.sh
# ======================
#SBATCH --job-name=test_job
#SBATCH --partition=teach_cpu
#SBATCH --account=phys040684
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:0:30
#SBATCH --mem=100M

# Load modules required for runtime either the module way:
# module add languages / python
# Or the Mamba way :
source ~/data-intensive-physics/initMamba.sh
mamba activate dip

# Changes directory to the one being looked at when the 
# job was submitted.
cd $SLURM_SUBMIT_DIR

# Now run your program with the usual command
python picalc_py3.py 10000000
python picalc_py4.py 10000000