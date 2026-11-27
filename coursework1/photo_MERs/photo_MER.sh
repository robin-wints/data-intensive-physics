#!/bin/bash
# ======================
# photo_MER.sh
# ======================
#SBATCH --job-name=photo_MER
#SBATCH --partition=teach_cpu
#SBATCH --account=phys040684
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:0
#SBATCH --mem=1000M
#SBATCH --output=photo_MERs/logs/slurm-%j.out
#SBATCH --error=photo_MERs/logs/slurm-%j.err

# Load modules required for runtime
source ~/initMamba.sh
mamba activate euclid

# Changes directory to project one
cd /user/home/nu23680/data-intensive-physics/coursework1

# Run programmes
python photo_MERs/photo_MER.py