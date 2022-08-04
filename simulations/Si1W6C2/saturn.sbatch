#!/bin/bash 

#SBATCH -p batch
#SBATCH -n 8
#SBATCH -N 2
#SBATCH --tasks-per-node=8
#SBATCH -t 0-00:30:00
#SBATCH --mem-per-cpu=1000M
#SBATCH -o log
#SBATCH --job-name="Si1W6C2"
#SBATCH --export=ALL

OUTDIR=/Users/bergstrom/GeneralAtomics/WSiC/simulations/Si1W6C2
RUNDIR=/cscratch/${USER}/${SLURM_JOBID}
mkdir -p ${RUNDIR}
mkdir ${RUNDIR}/results

cp -a ${OUTDIR}/input ${RUNDIR}/
cd ${RUNDIR}

# #Required modules
module load abinit
module load gcc7
#module load gcc-4.7.2
#module load mpich/3.2-gcc4.7.2
#module load fftw/3.3.6-mpich3.2-gcc4.7.2
#module load netcdf/4.4.1-mpich3.2-gcc4.7.2

srun --mpi=pmi2 -n 16 abinit < ./input/Si1W6C2.files > ./results/log

cp -a ${RUNDIR}/results ${OUTDIR}/
rm -rf ${RUNDIR}
