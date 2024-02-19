from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from scipy import integrate
#from sauron_colormap import sauron
import pandas as pd
import math


def smooth_mask(cube,beam,chans2look,rmsfac=3):
    mask=ndimage.uniform_filter(cube,size=[4,beam*1.5,beam*1.5])
    quart=np.floor(np.array(cube.shape)/8.).astype(np.int)
    half=np.floor(np.array(cube.shape)/2.).astype(np.int)
    #print(half, quart)
    rms=np.nanstd(mask[chans2look[0]:chans2look[1],half[1]-quart[1]:half[1]+quart[1],half[2]-quart[2]:half[2]+quart[2]])
    return mask>rms*rmsfac

def spectrum(cube):
    spec=np.nansum(np.nansum(cube,axis=1),axis=1)
    return spec

def mom_0(cube):
    m0=(cube).sum(axis=0)
    return m0

Gal=['HE0108','HE0433','HE1353','HE1108','HE1029']
Mol=['CS','HCO','HCN']

for i in range(len(Gal)):
    for j in range(len(Mol)):
        hdu=fits.open('/Users/jelford/Documents/PhD_Work/CARS_Data/'+str(Gal[i])+'/'+str(Gal[i])+'_clean_'+str(Mol[j])+'.image.fits')

        data=hdu[0].data
        datan=np.squeeze(data)
        datann=np.nan_to_num(datan)

        hdr=hdu[0].header
        beamtab=hdu[1].data

        bmajas=np.median(beamtab['BMAJ'])
        bmaj=bmajas/3600

        mask=smooth_mask(datann,bmaj/np.abs(hdr['CDELT1']),[1,10],rmsfac=1.5)
        datamask=datann*mask

        m0=mom_0(datamask)
        plt.imshow(m0)
        plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/'+str(Gal[i])+'/'+str(Gal[i])+'_'+str(Mol[j])+'_moment_0_whole.png',bbox_inches='tight')
        plt.close()

        spec=spectrum(datann)
        plt.step(np.arange(spec.shape[0]),spec)
        plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/'+str(Gal[i])+'/'+str(Gal[i])+'_'+str(Mol[j])+'_spec_whole.png',bbox_inches='tight')
        plt.close()
