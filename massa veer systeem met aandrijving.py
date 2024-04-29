# -*- coding: utf-8 -*-
"""
@author: cookie monster
"""

import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("dark_background")
df = pd.read_csv(r"C:\Users\User\Downloads\posities\Posities\posities_2_Team_01.txt", names=["t", "position"], sep='   ', engine="python")

v = np.gradient(df["position"], df["t"])
a = np.gradient(v, df["t"])
t = df["t"]

m = 1.3837e-6
b = 0.032215
k = 30

def dxdt(x,a):
    dx_dt=np.array([0.,0.])
    dx_dt[0]= x[1]
    dx_dt[1]= a-b/m*x[1]-k/m*x[0]
    return dx_dt

def Euler(a):
    x=np.zeros([len(t),2])
    x[0,:]=np.array([0,0])
    
    for i,tval in enumerate(t[:-1]):
        x[i+1,:]=x[i,:]+(t[i+1]-t[i])*dxdt(x[i,:],a[i])
    return x

x=Euler(a)

fig, ax = plt.subplots()
ax.plot(t, x[:,0], label = "locatie massa ")
ax2 = ax.twinx()
ax2.plot(df["t"], a, c="orange", label = "versnelling doos")
plt.legend()
plt.show()
