#!/bin/bash
# ======================
# mpi_pi_script.sh
# ======================
#SBATCH --job-name=mpi_picalc
#SBATCH --partition=teach_cpu
#SBATCH --account=phys040684
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=24
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:0
#SBATCH --mem=1000M

# Load modules required for runtime
source ~/data-intensive-physics/initMamba.sh
mamba activate mpi

# Changes directory to the one being looked at when the 
# job was submitted.
cd $SLURM_SUBMIT_DIR

# Run programmes
for i in {2..48..2}
do 
    mpirun --bind-to none -np $i python mpi_pi_reduce_v2.py 
done