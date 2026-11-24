#!/bin/bash
# ======================
# mosaics.sh
# ======================
#SBATCH --job-name=mosaic
#SBATCH --partition=teach_cpu
#SBATCH --account=phys040684
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:0
#SBATCH --mem=1000M
#SBATCH --output=mosaics/logs/slurm-%j.out
#SBATCH --error=mosaics/logs/slurm-%j.err

# Load modules required for runtime
source ~/initMamba.sh
mamba activate euclid

# Changes directory to the one being looked at when the 
# job was submitted.
cd $SLURM_SUBMIT_DIR

# Run programmes
python mosaics/mosaics.py