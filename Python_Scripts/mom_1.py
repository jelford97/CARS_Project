import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from sauron_colormap import sauron
from scipy import ndimage

def smooth_mask(cube,beam,chans2look,rmsfac=3):
    mask=ndimage.uniform_filter(cube,size=[4,beam*1.5,beam*1.5])
    quart=np.floor(np.array(cube.shape)/8.).astype(np.int)
    half=np.floor(np.array(cube.shape)/2.).astype(np.int)
    #print(half, quart)
    rms=np.nanstd(mask[chans2look[0]:chans2look[1],half[1]-quart[1]:half[1]+quart[1],half[2]-quart[2]:half[2]+quart[2]])
    return mask>rms*rmsfac

hdu=fits.open('/Users/jelford/Documents/PhD_Work/CARS_Data/HE11082813/cleanco.fits')
data=hdu[0].data
datan=np.squeeze(data)
#datann=np.nan_to_num(datan)
hdr=hdu[0].header
beamtab=hdu[1].data
bmajas=np.median(beamtab['BMAJ'])
bminas=np.median(beamtab['BMIN'])
bmaj=bmajas/3600
bmin=bminas/3600
mask=smooth_mask(datan,bmaj/np.abs(hdr['CDELT1']),[1,20],rmsfac=3)
maskcube=datan*mask

v=np.arange(-2430,2430,20)

def mom_1(cube,v):
    m1=(cube.T*v).sum(axis=2)/(cube).sum(axis=0)
    return m1

m1=mom_1(maskcube,v)

plt.imshow(m1,vmax=100, vmin=-100, cmap=sauron)
plt.xlabel('RA(pixels)')
plt.ylabel('DEC(pixels)')
plt.colorbar(label='Velocity(km/s)')
plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/HE11082814mom1.png',bbox_inches='tight')
