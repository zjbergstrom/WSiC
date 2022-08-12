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
    print(structure.strip())
    structure = structure.strip()
    os.system("grep 'etotal  ' {}/{}/{}/results/log > {}.tmp".format(pwd,rundir,structure,structure))
    try:
        z = genfromtxt("{}.tmp".format(structure))
        e.append(z[1])
    except IndexError:
        print("empty file, skipping structure {}".format(structure))
        e.append(0)
    else:
        print("not an empty file!")
        z = genfromtxt("{}.tmp".format(structure))
        e.append(z[1])
        

# try to open the file, it True, append, if False, write
filename = "structure_energies.dat"
DNF = []
try:
    print("Trying to open the file...")
    instr = open(filename,"r")
except:
    # Write structures and energies into a file
    print("File not found. Writing {}".format(filename))
    with open(filename,"w") as fout:
        for i,structure in enumerate(structures):
            fout.write("{} {}\n".format(structure.strip(),e[i]))
else:
    # Append structures and energies into a file
    print("File found! Appending...")
    with open("structure_energies.dat","a") as fout:
        for i,structure in enumerate(structures):
            if i==0:
                fout.write("structure energy\n")
            if e[i] != 0:
                fout.write("{} {}\n".format(structure.strip(),e[i]))
            else:
                DNF.append(structure.strip())
#print("DNF:",DNF)
print(len(DNF),"structures out of",len(structures),"did not finish")
np.savetxt("DNF.txt",DNF,fmt="%s")

# Clean up
os.system("rm *.tmp")
