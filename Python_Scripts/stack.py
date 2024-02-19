from stackarator import stackarator
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import astropy.units as u
import pandas as pd
from astropy.coordinates import SpectralCoord
from gastimator import gastimator

stack=stackarator()
data=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/Stacking_Parameters.csv')
galaxy=data['Galaxy']
cubepath=data['Cube path']
mom1path=data['Moment 1 Path']
rvel=data['Recession Velocity']
radiovel=data['Radio Velocity']
Line=data['Line']
Stack_Data=data['Stacking Data']
RA=data['RA']
DEC=data['DEC']
pix=data['Cellsize']
Xmin=data['Xmin']
Xmax=data['Xmax']
Ymin=data['Ymin']
Ymax=data['Ymax']
Restfreq=data['Rest Freq (GHz)']


for i in range(len(galaxy)):
    if Stack_Data[i]=='CO':
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
        print(outn)
        plt.plot(vout,outspec,drawstyle='steps-mid')
        plt.xlabel("Velocity (km/s)")
        plt.ylabel("Intensity (Jy/beam)")
        plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/Stacked_Spectra/Spectra'+str(galaxy[i])+str(Line[i])+'_stacked.png',bbox_inches='tight')
        plt.close()
        hdu=fits.PrimaryHDU(Spec)
        hdu.writeto('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/Stacked_Spectra/Spectra'+str(galaxy[i])+str(Line[i])+'_stacked.fits',overwrite=True)
        #print(outrms)
        #Gauss_Fit=fit_single(vout,outspec,outrms)
        #print(Gauss_Fit)
    else:
        stack.read_fits_cube(cubepath[i])
        Musehdu=fits.open(mom1path[i])
        MuseData=Musehdu[0].data
        sc4= SpectralCoord(MuseData*u.km/u.s,doppler_convention='optical',doppler_rest=6e5*u.GHz)
        v1=sc4.to(u.km/u.s,doppler_convention='radio').value
        DataShape=MuseData.shape
        RAgal=RA[i]
        DECgal=DEC[i]
        Cell=pix[i]
        Xarr=np.arange(Xmin[i],Xmax[i])*Cell+RAgal
        Yarr=np.arange(Ymin[i],Ymax[i])*Cell+DECgal
        stack.input_mom1(Xarr,Yarr,v1)
        vout,outspec,outrms,outn=stack.stack()
        print(outn)
        voutshape=np.array(vout.shape)
        outspecshape=np.array(outspec.shape)
        outrmsshape=np.array(outrms.shape)
        outnshape=np.array(outn.shape)
        voutn=(vout.reshape(voutshape[0],1))
        outspecn=(outspec.reshape(outspecshape[0],1))
        outrmsn=(outrms.reshape(outrmsshape[0],1))
        outnn=(outn.reshape(outnshape[0],1))
        Spec=np.concatenate((voutn,outspecn,outrmsn,outnn),axis=1)
        plt.plot(vout,outspec,drawstyle='steps-mid')
        plt.xlabel("Velocity (km/s)")
        plt.ylabel("Intensity (Jy/beam)")
        plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/Stacked_Spectra/Spectra'+str(galaxy[i])+str(Line[i])+'_stacked.png',bbox_inches='tight')
        plt.close()
        hdu=fits.PrimaryHDU(Spec)
        hdu.writeto('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/Stacked_Spectra/Spectra'+str(galaxy[i])+str(Line[i])+'_stacked.fits',overwrite=True)
        
        #print(outrms)
        #Gauss_Fit=fit_single(voutn,outspecn,outrms)
        #print(Gauss_Fit)