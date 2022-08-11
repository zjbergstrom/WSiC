import os
import numpy as np
from numpy import genfromtxt

pwd = os.environ["PWD"]

instr=open("submit_dirs.txt",'r')
structures=instr.readlines()

# Collect energies
e = []
for structure in structures:
    print(structure.strip())
    structure = structure.strip()
    os.system("grep etotal {}/simulations/{}/results/log > {}.tmp".format(pwd,structure,structure))
    z = genfromtxt("{}.tmp".format(structure))
    if len(z) == 0:
        e.append(0)
    else:
        # print(z,z[0],z[1])
        e.append(z[1])

# try to open the file, it True, append, if False, write
filename = "structure_energies.dat"
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
    with open("structure_energies.dat","w") as fout:
        for i,structure in enumerate(structures):
            if i==0:
                fout.write("structure energy\n")
            fout.write("{} {}\n".format(structure.strip(),e[i]))

# # Write structures and energies into a file
# with open("structure_energies.dat","w") as fout:
#     for i,structure in enumerate(structures):
#         fout.write("{} {}\n".format(structure.strip(),e[i]))

# Clean up
os.system("rm *.tmp")