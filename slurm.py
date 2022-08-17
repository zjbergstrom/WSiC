import os
import generate_files as gf
import numpy as np
from numpy import genfromtxt
pwd = os.environ["PWD"]

# Iris: 16 cpus per node
# Saturn: 8 cpus per node
cpus = {"saturn" : 8, "iris" : 16}
q = {"saturn" : "batch", "iris" : "short"}

def writeSubmitScript(cluster="saturn", script_name = "saturn.sbatch", job_name="job name", queue = None, nodes=2, hrs=0, mins=30, rundir="simulations"):
    with open(script_name,"w") as fout:
        fout.write('#!/bin/bash \n\n')

        if queue is not None: fout.write('#SBATCH -p {}\n'.format(queue))
        else: fout.write('#SBATCH -p {}\n'.format(q[cluster]))
        fout.write('#SBATCH -n {}\n'.format(cpus[cluster]))
        fout.write('#SBATCH -N {}\n'.format(nodes))
        fout.write('#SBATCH --tasks-per-node={}\n'.format(cpus[cluster]))
        fout.write('#SBATCH -t 0-{}:{}:00\n'.format(hrs,mins))
        fout.write('###SBATCH --mem-per-cpu=1000M\n')
        fout.write('#SBATCH -o log\n')
        fout.write('#SBATCH --job-name="{}"\n'.format(job_name))
        fout.write('#SBATCH --export=ALL\n\n')

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
        fout.write('srun --mpi=pmi2 -n {} abinit < ./input/{}.files > ./results/log\n\n'.format(nodes*cpus[cluster],job_name))

        fout.write('cp -a ${RUNDIR}/results ${OUTDIR}/\n')
        fout.write('rm -rf ${RUNDIR}\n')

if __name__ == "__main__":
    structs = gf.getStructures(filename="filenames1.txt",dir="structurefiles/")
    base_structs = gf.getStructures(filename="filenames0.txt",dir="structurefiles/")
    structs = structs + base_structs
    filename = "DNF.txt"
    instr = open(filename,"r")
    DNF = instr.read().splitlines()
    rundir = "simulations"
    for struct in structs:
        name = struct.composition.formula.replace(" ","")
        if name in DNF:
            print("Found",name,"in {}.".format(filename))
            writeSubmitScript(cluster="saturn", script_name="saturn.sbatch", job_name=name, \
                                rundir=rundir, nodes=4, hrs=1, mins=00)
            os.system("mv saturn.sbatch {}/{}".format(rundir,name))
