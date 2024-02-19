import numpy as np
from decimal import Decimal



def B_temp(I,BMAJ,BMIN,freq,dist):
    QF=1.222e3*(1/((freq)**2)*BMAJ*BMIN)
    I_mjy=I*1e3
    I_K=I_mjy*QF
    beam_area=(4.84*dist*BMAJ)*(4.84*dist*BMIN)
    L_K=I_K*beam_area
    return L_K

Galaxies=['IRAS 20551−4250','NGC1614','IRAS 08572+3915 NW','IRAS 12127−1412 NE','IRAS 00183−7111','IRAS 22491−1808']

HCN=[8.1,1.7,2.8,1.1,0.70,7.1]
HCO=[12,7.1,3.5,0.56,0.57,4.7]
HCN_BMAJ=[0.6,1.5,1.8,0.6,2.4,0.6]
HCN_BMIN=[0.4,1.3,1.1,0.5,1.2,0.6]
HCO_BMAJ=[0.6,1.5,2.5,0.6,2.3,0.6]
HCO_BMIN=[0.4,1.3,1.1,0.5,1.2,0.5]
HCN_freq=354.505
HCO_freq=356.734
z=np.array([0.043,0.016,0.058,0.133,0.327,0.076])

H0=70
c=3e5
dist=(c*z)/H0

L_HCN=[]
L_HCO=[]
for i in range(len(HCN)):
    LkHCN=B_temp(HCN[i],HCN_BMAJ[i],HCN_BMIN[i],HCN_freq,dist[i])
    L_HCN.append(LkHCN)
    LkHCO=B_temp(HCO[i],HCO_BMAJ[i],HCO_BMIN[i],HCO_freq,dist[i])
    L_HCO.append(LkHCO)

print(np.array(L_HCN)/1e6)
print(np.array(L_HCO)/1e6)