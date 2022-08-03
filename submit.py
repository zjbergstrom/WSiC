import os

pwd = os.environ["PWD"]
os.system("ls simulations > submit_dirs.txt")

instr=open("submit_dirs.txt",'r')
submissions=instr.readlines()

structures = []
for submission in submissions:
	os.system("sbatch simulations/{}/saturn.sbatch".format(submission.strip()))

