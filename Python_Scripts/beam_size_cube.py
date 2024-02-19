from astropy.io import fits
import numpy as np

hdu=fits.open('/Users/jelford/Documents/PhD_Work/CARS_Data/HE1353/HE13531917_clean_co.image.fits')
beamtab=hdu[1].data
bmaj=np.median(beamtab['BMAJ'])
bmin=np.median(beamtab['BMIN'])

beam_size=np.sqrt(bmaj*bmin)

print(beam_size)