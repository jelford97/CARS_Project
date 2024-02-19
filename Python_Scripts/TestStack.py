from stackarator import stackarator
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import pandas as pd

mom1=fits.open('/Users/jelford/Documents/PhD_Work/CARS_Data/HE11082813/HE1108_mom1.fits')
mom1hdr=mom1[0].header
stack=stackarator()
stack.read_fits_cube('/Users/jelford/Documents/PhD_Work/CARS_Data/HE11082813/cleanco.fits')
stack.read_fits_mom1('/Users/jelford/Documents/PhD_Work/CARS_Data/HE11082813/HE1108_mom1.fits')


vout,outspec,outrms,outn = stack.stack()
voutshape=np.array(vout.shape)
outspecshape=np.array(outspec.shape)
voutn=vout.reshape(voutshape[0],1)
outspecn=outspec.reshape(outspecshape[0],1)
Spec=np.concatenate((voutn,outspecn),axis=1)
plt.plot(vout,outspec,drawstyle='steps-mid')
plt.xlabel("Velocity (km/s)")
plt.ylabel("Intensity (Jy/beam)")
plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/Stacked_Spectra/Stacked_CO.png',bbox_inches='tight')
plt.close()
    
