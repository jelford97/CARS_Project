from stackarator import stackarator
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import astropy.units as u
import pandas as pd
from astropy.coordinates import SpectralCoord
from gastimator import gastimator

data=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/CO_stack.csv')

galaxy=data['Galaxy']
cubepath=data['Cube path']
mom1path=data['Moment 1 Path']

stack=stackarator()
for i in range(len(galaxy)):
    stack.read_fits_cube(cubepath[i])
    stack.read_fits_mom1(mom1path[i])
    vout,outspec,outrms,outn = stack.stack()
    voutshape=np.array(vout.shape)
    outspecshape=np.array(outspec.shape)
    outrmsshape=np.array(outrms.shape)
    outnshape=np.array(outn.shape)
    voutn=(vout.reshape(voutshape[0],1))
    outspecn=(outspec.reshape(outspecshape[0],1))
    outrmsn=(outrms.reshape(outrmsshape[0],1))
    outnn=(outn.reshape(outnshape[0],1))
    Spec=np.concatenate((voutn,outspecn,outrmsn,outnn),axis=1)
    #print(outn)
    plt.plot(vout,outspec,drawstyle='steps-mid')
    plt.xlabel("Velocity (km/s)")
    plt.ylabel("Intensity (Jy/beam)")
    plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/Stacked_Spectra/Spectra'+str(galaxy[i])+'CO_13__stacked.png',bbox_inches='tight')
    plt.close()
    hdu=fits.PrimaryHDU(Spec)
    hdu.writeto('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/Stacked_Spectra/Spectra'+str(galaxy[i])+'CO_13__stacked.fits',overwrite=True)
