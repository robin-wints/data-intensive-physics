#!/bin/bash
# ======================
# color_hist.sh
# ======================
#SBATCH --job-name=SED
#SBATCH --partition=teach_cpu
#SBATCH --account=phys040684
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:5:0
#SBATCH --mem=100M
#SBATCH --output=photoz_PHZ/logs/slurm-%j.out
#SBATCH --error=photoz_PHZ/logs/slurm-%j.err

# Load modules required for runtime
source ~/initMamba.sh
mamba activate euclid

# Changes directory to the one being looked at when the 
# job was submitted.
cd $SLURM_SUBMIT_DIR

# Run programmes
python photoz_PHZ/colour_hist.py 