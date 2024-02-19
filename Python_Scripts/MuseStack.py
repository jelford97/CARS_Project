from stackarator import stackarator
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

mom1=fits.open('/Users/jelford/Documents/PhD_Work/CARS_Data/HE10291831/HE1029MuseMom1.fits')
mom1dat=mom1[0].data
xsize=np.arange(-157,157)
ysize=np.arange(-158,159)
stack=stackarator()
stack.read_fits_cube('/Users/jelford/Documents/PhD_Work/CARS_Data/HE10291831/HE1029_CS_clean.fits')
stack.input_mom1(xsize,ysize,mom1dat.T)
vout,outspec,outrms,outn=stack.stack()

plt.plot(vout,outspec,drawstyle='steps-mid')
plt.xlabel("Velocity (km/s)")
plt.ylabel("Intensity (Jy/beam)")
plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/Stacked_Spectra/HE10291831_HCN_MuseStack.png')
plt.show()