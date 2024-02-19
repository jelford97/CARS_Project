import pandas as pd
import numpy as np
from astropy.io import fits

param=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/G_S_Param.csv')
filepath=np.array(param['File Path'])


bmajas_L=[]
bminas_L=[]
restfrq_L=[]
QFAC=[]
for i in range(len(filepath)):
    hdu=fits.open(filepath[i])
    hdr=hdu[0].header
    btab=hdu[1].data
    bmajas=np.median(btab['BMAJ'])
    bminas=np.median(btab['BMIN'])
    bmajas_L.append(bmajas)
    bminas_L.append(bminas)
    restfrq=np.array(hdr['RESTFRQ'])/1e9
    restfrq_L.append(restfrq)
    Q_fac=1.222e3*(1/((restfrq**2)*bminas*bmajas))
    QFAC.append(Q_fac)


param['Beam Width Major']=bmajas_L
param['Beam Width Minor']=bminas_L
param['Rest Freq (GHz)']=restfrq_L
param['Q_Factor']=QFAC

param.to_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/G_S_Param.csv',index=False)
