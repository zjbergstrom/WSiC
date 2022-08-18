from ast import Not
import os
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

import datetime
import time



pwd = os.environ["PWD"]

instr=open("submit_dirs.txt",'r')
structures=instr.readlines()

rundir = "simulations"

# Collect energies
# WHAT IF I STORED THE STRUCTS AND ENERGIES IN A RESULTS DICT???
results = {}
e = []
scfcv = []
for structure in structures:
    structure = structure.strip()
    log_dir = "{}/{}/{}/results/log".format(pwd,rundir,structure)
    try:
        logfile = open(log_dir).readlines()
    except FileNotFoundError:
        print("{} does not exist.".format(structure))
        e.append('DNE')
    else:
        NotFound = True
        NotConv = True
        for line in logfile:
            line = line.strip()
            if "gradients are converged" in line:
                print("{} is converged!.".format(structure))
                NotConv = False
            if "etotal  " in line and NotConv==False:
                NotFound = False
                line = line.split()
                print(structure,line[1])
                e.append(line[1])
            if "scfcv: " in line:
                line = line.split()
                try:
                    scfcv.append(int(line[4]))
                except ValueError:
                    x = time.strptime(line[4],'%M:%S')
                    scfcv.append(datetime.timedelta(minutes=x.tm_min,seconds=x.tm_sec).total_seconds())

        if NotConv:
            print("{} did not converge.".format(structure))
            e.append('DNC')
        elif NotFound:
            print("{} did not finish.".format(structure))
            e.append('DNF')
        # print("\n=============================")
        # print("Simulations details:")
        # print("-----------------------------")
        # os.system("grep etotal {}".format(log_dir))
        # print("-----------------------------")
        # os.system("grep gradients {}".format(log_dir))

plt.hist(scfcv)
plt.show()

filename = "structure_energies.dat"
DNF = []

try:
    print("Trying to open the file...")
    instr = open(filename,"r")

except:
    with open(filename,"w") as fout:
        for i,structure in enumerate(structures):
            energy = e[i]
            if i==0:
                fout.write("structure energy\n")
            # if the calculation completed, record the structure and energy
            if energy != 'DNE' and energy != 'DNF':
                fout.write("{} {}\n".format(structure.strip(),e[i]))
            # if the calculation did not complete, add the structure to DNF list
            else:
                DNF.append(structure.strip())

else:
    # Append structures and energies into a file
    print("Appending energies to existing file...")
    with open("structure_energies.dat","a") as fout:
        for i,structure in enumerate(structures):
            # if the calculation completed, record the structure and energy
            if e[i] != 0:
                fout.write("{} {}\n".format(structure.strip(),e[i]))
            # if the calculation did not complete, add the structure to DNF list
            else:
                DNF.append(structure.strip())

#print("DNF:",DNF)
print(len(DNF),"structures out of",len(structures),"did not finish")
np.savetxt("DNF.txt",DNF,fmt="%s")


