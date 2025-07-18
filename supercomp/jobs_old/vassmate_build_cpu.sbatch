#!/bin/bash

#SBATCH --job-name=vassmate_test
#SBATCH --output=logs/vassmate_%j.out
#SBATCH --error=logs/vassmate_%j.err
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=4G

echo "Job Started at $(date)!"

apptainer build --fakeroot --force /home/vassmate/KGEntityMatching/envs/vassmate_container.sif /home/vassmate/KGEntityMatching/envs/vassmate_container.def

echo "Job Finished at $(date)!"
