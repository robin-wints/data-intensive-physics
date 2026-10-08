#!/bin/bash
# ======================
# serialscript.sh
# ======================
#SBATCH --job-name=test_job
#SBATCH --partition=teach_cpu
#SBATCH --account=phys040684
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:0
#SBATCH --mem=1000M

# Load modules required for runtime
source ~/data-intensive-physics/initMamba.sh
mamba activate dip

# Changes directory to the one being looked at when the 
# job was submitted.
cd $SLURM_SUBMIT_DIR

# Run programmes
for i in {1..24}
do 
    python picalc_multiproc.py 100000000 $i 
done