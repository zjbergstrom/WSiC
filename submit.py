import os

pwd = os.environ["PWD"]
rundir = "simulations"

os.system("ls {} > submit_dirs.txt".format(rundir))

filename = "submit_dirs.txt"
instr=open(filename,'r')
# instr = open("DNF.txt")
submissions=instr.readlines()

structures = []
for submission in submissions:
	os.system("sbatch {}/{}/abinit.sbatch".format(rundir,submission.strip()))

print("submitted",len(structures),"jobs")

