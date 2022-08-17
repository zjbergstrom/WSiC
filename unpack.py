import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle("enthalpy.pkl")
print(df)

data = df["formation enthalpy"]
d=[]
for dat in data:
    if dat < 3:
        d.append(dat)


plt.hist(d)
plt.show()
