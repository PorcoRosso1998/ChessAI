#!/bin/bash
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=4
#SBATCH --time=00:01:00
#SBATCH --output=mpijob.out
#SBATCH --error=mpijob.err

mpiexec -n $SLURM_NTASKS python3 AlphaBetaPruning.py



