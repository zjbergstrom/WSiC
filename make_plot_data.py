import pandas as pd
import numpy as np
from numpy import genfromtxt
import os

filename_s = "structure_data.pkl"
filename_e = "Structure_energies.dat"
df_s = pd.read_pickle(filename_s)
print(df_s)

df_s["energy"] = None

instr=open(filename_e,'r')
data=instr.readlines()

for datum in data:
    dat = datum.split()
    df_s.loc[df_s["structure"] == dat[0], "energy"] = float(dat[1])

print(df_s)

np.savetxt('e.txt', df_s["energy"].values)
np.savetxt('w.txt', df_s["W"].values)
np.savetxt('si.txt', df_s["Si"].values)
np.savetxt('c.txt', df_s["C"].values)

os.system("paste e.txt w.txt si.txt c.txt > plot_data.txt")
os.system("rm e.txt w.txt si.txt c.txt")


