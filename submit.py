import os

pwd = os.environ["PWD"]
rundir = "simulations"

os.system("ls {} > submit_dirs.txt".format(rundir))

instr=open("submit_dirs.txt",'r')
# instr = open("DNF.txt")
submissions=instr.readlines()

structures = []
for submission in submissions:
	os.system("sbatch {}/{}/saturn.sbatch".format(rundir,submission.strip()))

