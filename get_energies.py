import os
import numpy as np
from numpy import genfromtxt

pwd = os.environ["PWD"]

instr=open("submit_dirs.txt",'r')
structures=instr.readlines()

rundir = "simulations"

# Collect energies
e = []
for structure in structures:
    structure = structure.strip()
    log_dir = "{}/{}/{}/results/log".format(pwd,rundir,structure)
    try:
        logfile = open(log_dir).readlines()
    except FileNotFoundError:
        print("No log file for structure {}! Appending 0 for the energy...".format(structure))
        e.append(0)
    else:
        NotFound = True
        for line in logfile:
            line = line.strip()
            if "etotal  " in line:
                NotFound = False
                line = line.split()
                print(structure,line[1])
                e.append(line[1])
        if NotFound:
            e.append(0)
        


filename = "structure_energies.dat"
DNF = []

try:
    print("Trying to open the file...")
    instr = open(filename,"r")

except:
    with open(filename,"w") as fout:
        for i,structure in enumerate(structures):
            if i==0:
                fout.write("structure energy\n")
            # if the calculation completed, record the structure and energy
            if e[i] != 0:
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


