from astropy.io import fits
data=fits.open('/Users/jelford/Documents/PhD_Work/CARS_Data/HE0108/HE0108-4743.MUSE.WFM-NOAO.maps-full.fits')

hdr=data[1].header
print(hdr)
mom1=data[1].data

#mom1map=fits.PrimaryHDU(mom1)
#mom1map.writeto('/Users/jelford/Documents/PhD_Work/CARS_Data/HE01084743/HE0108MuseMom1.fits')
