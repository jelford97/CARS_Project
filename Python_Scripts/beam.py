import numpy as np
from astropy.io import fits
import math

hdu=fits.open('/Users/jelford/Documents/PhD_Work/CARS_Data/Cont_images/HE01084743_dense_cont.image.fits')

header=hdu[0].header
#print(header)
#beamtab=hdu[1].data

xcellsize=header['CDELT1']
bmaj=header['BMAJ']
bmin=header['BMIN']
#bmaj=bmajas/3600
#bmin=bminas/3600

invbeam=(math.pi*(bmaj/np.abs(xcellsize))*(bmin/np.abs(xcellsize)))/(4*np.log(2))

beam=1/invbeam

print(beam)