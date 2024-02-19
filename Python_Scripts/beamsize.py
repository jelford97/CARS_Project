import numpy as np

z=np.array([0.024,0.036,0.041,0.024,0.035])
beam_dense=np.array([0.750,0.863,0.748,0.814,0.704])
beam_CO=np.array([0.447,0.571,0.587])
z_CO=np.array([0.036,0.024,0.035])

H0=70
c=3e5

dist_Mpc=(c*z)/H0
dist_Mpc_CO=(c*z_CO)/H0

phy_size=4.84*dist_Mpc*beam_dense
phy_size_CO=4.84*dist_Mpc_CO*beam_CO

print(phy_size)
print(phy_size_CO)