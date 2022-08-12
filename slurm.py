import os
import generate_files as gf
import numpy as np
from numpy import genfromtxt
pwd = os.environ["PWD"]


def writeSubmitScript(cluster="saturn", script_name = "saturn.sbatch", job_name="job name", nodes=2, hrs=0, mins=30, rundir="simulations"):
    with open(script_name,"w") as fout:
        if cluster=="saturn":
            fout.write('#!/bin/bash \n\n')
            fout.write('#SBATCH -p batch\n')
            fout.write('#SBATCH -n 8\n')
            fout.write('#SBATCH -N {}\n'.format(nodes))
            fout.write('#SBATCH --tasks-per-node=8\n')
            fout.write('#SBATCH -t 0-{}:{}:00\n'.format(hrs,mins))
            fout.write('###SBATCH --mem-per-cpu=1000M\n')
            fout.write('#SBATCH -o log\n')
            fout.write('#SBATCH --job-name="{}"\n'.format(job_name))
            fout.write('#SBATCH --export=ALL\n\n')
        elif cluster=="iris":
            fout.write('#!/bin/bash\n\n')
            fout.write('#SBATCH -p short\n')
            fout.write('#SBATCH -n 1\n')
            fout.write('#SBATCH -N 1\n')
            fout.write('#SBATCH --tasks-per-node=8\n')
            fout.write('#SBATCH -t 0-00:30:00\n')
            fout.write('###SBATCH --mem-per-cpu=1000M\n')
            fout.write('#SBATCH -o log\n')
            fout.write('#SBATCH --job-name="{}"\n'.format(job_name))
            fout.write('#SBATCH --export=ALL\n')


        fout.write('OUTDIR={}/{}/{}\n'.format(pwd,rundir,job_name))
        fout.write('RUNDIR=/cscratch/${USER}/${SLURM_JOBID}\n')
        fout.write('mkdir -p ${RUNDIR}\n')
        fout.write('mkdir ${RUNDIR}/results\n\n')

        fout.write('cp -a ${OUTDIR}/input ${RUNDIR}/\n')
        fout.write('cd ${RUNDIR}\n\n')

        fout.write('# #Required modules\n')
        fout.write('module load abinit\n')
        fout.write('module load gcc7\n')
        fout.write('#module load gcc-4.7.2\n')
        fout.write('#module load mpich/3.2-gcc4.7.2\n')
        fout.write('#module load fftw/3.3.6-mpich3.2-gcc4.7.2\n')
        fout.write('#module load netcdf/4.4.1-mpich3.2-gcc4.7.2\n\n')

        #fout.write('mkdir results\n')
        fout.write('srun --mpi=pmi2 -n {} abinit < ./input/{}.files > ./results/log\n\n'.format(nodes*8,job_name))

        fout.write('cp -a ${RUNDIR}/results ${OUTDIR}/\n')
        fout.write('rm -rf ${RUNDIR}\n')

if __name__ == "__main__":
    structs = gf.getStructures(filename="filenames0.txt",dir="structurefiles/")
    DNF = genfromtxt("DNF.txt")
    rundir = "simulations"
    for struct in structs:
        if struct in DNF:
            name = struct.composition.formula.replace(" ","")
            writeSubmitScript(cluster="saturn", script_name="saturn.sbatch", job_name=name, \
                                rundir=rundir, nodes=None, cpus=None, hrs=0, mins=30)
            os.system("mv saturn.sbatch {}/{}".format(rundir,name))
