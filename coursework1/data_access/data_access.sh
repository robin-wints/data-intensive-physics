#!/bin/bash
# ======================
# data_access.sh
# ======================
#SBATCH --job-name=q1_data
#SBATCH --partition=teach_cpu
#SBATCH --account=phys040684
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:0
#SBATCH --mem=1000M
#SBATCH --output=data_access/logs/slurm-%j.out
#SBATCH --error=data_access/logs/slurm-%j.err

# Load modules required for runtime
source ~/initMamba.sh
mamba activate euclid

# Changes directory to the one being looked at when the 
# job was submitted.
cd $SLURM_SUBMIT_DIR

# Run programmes
python data_access/data_access.py --login_file ./login.txt --output_dir ./data 