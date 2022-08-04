import os

pwd = os.environ["PWD"]

instr=open("submit_dirs.txt",'r')
structures=instr.readlines()

# Collect energies
e = []
for structure in structures:
    structure = structure.strip()
    os.system("grep etotal {}/simulations/{}/results/log > {}.tmp".format(pwd,structure,structure))
    dd=open("{}.tmp".format(structure),'r')
    d=dd.readlines()
    e.append(d[1])

# Write structures and energies into a file
with open("structure_energies.dat","w") as fout:
    for i,structure in enumerate(structures):
        fout.write("{} {}\n".format(structure.strip(),e[i]))

# Clean up
os.system("rm *.tmp")