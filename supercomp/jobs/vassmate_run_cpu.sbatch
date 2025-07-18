#!/bin/bash

#SBATCH --job-name=vassmate_cpu
#SBATCH --output=logs/vassmate_%j.out
#SBATCH --error=logs/vassmate_%j.err
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=4G

echo "Job Started at $(date)!"

apptainer run --bind /home/vassmate/KGEntityMatching/_input:/hdd /home/vassmate/KGEntityMatching/envs/vassmate_container.sif python3 /home/vassmate/KGEntityMatching/_pipeline_node_reranker.py

echo "Job Finished at $(date)!"
