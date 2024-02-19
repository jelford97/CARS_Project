from astropy.io import fits
import numpy as np

hdu=fits.open('/Users/jelford/Documents/PhD_Work/CARS_Data/HE1353/HE13531917_clean_co.image.fits')
data=hdu[0].data

def rms_estimate(cube,chanstart,chanend):
        quarterx=np.array(cube.shape[0]/4.).astype(int)
        quartery=np.array(cube.shape[1]/4.).astype(int)
        return np.nanstd(cube[quarterx*1:3*quarterx,1*quartery:3*quartery,chanstart:chanend])

rms=rms_estimate(data.T,2,5)

print(rms)