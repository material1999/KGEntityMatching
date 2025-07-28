#!/bin/bash

#SBATCH --job-name=vass_stexpanded_memoryalpha
#SBATCH --output=logs/vassmate_%j.out
#SBATCH --error=logs/vassmate_%j.err
#SBATCH --partition=all
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=4G
#SBATCH --gres=gpu:4

echo "Job Started at $(date)!"

apptainer run --nv --bind /home/vassmate/KGEntityMatching/_input:/hdd /home/vassmate/KGEntityMatching/envs/vassmate_container.sif python3 /home/vassmate/KGEntityMatching/stexpanded_memoryalpha.py

echo "Job Finished at $(date)!"
