from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

def sigma_clip(data,err,fac):
    sn=data/err
    mask=np.where(sn>fac,1,np.NaN)
    mask_data=data*mask
    return mask_data

Galaxy_maps=['HE0108-4743','HE0433-1028','HE1353-1917','HE1108-2813','HE1029-1831']
Galaxy_abr=['HE0108','HE0433','HE1353','HE1108','HE1029']
beam=[0.78,1.03,0.77,1.00,0.82]

z=np.array([0.023928,0.035536,0.034811,0.040501,0.023953])
H0=70
c=3e5
Dist=(c*z)/H0

def dist(NX,NY,beamsize,RApixel,DECpixel,C):
        X=np.arange(NX)
        Y=np.arange(NY)
        RAaxis=np.abs(((X-RApixel)*C))
        DECaxis=np.abs(((Y-DECpixel)*C))
        im=np.empty([NY,NX])
        for i in range(0,NX):
            for j in range(0,NY):
                im[j,i]=np.sqrt(RAaxis[i]**2+DECaxis[j]**2)
        return im<beamsize

SFR=[]
for i in range(len(Galaxy_maps)):
    hdu=fits.open('/Users/jelford/Documents/PhD_Work/CARS_Data/'+str(Galaxy_abr[i])+'/'+str(Galaxy_maps[i])+'.MUSE.WFM-NOAO.maps-full.fits')

    hdr=hdu[11].header
    Halpha=hdu[9].data
    Halphaerr=hdu[10].data
    Halphamask_data=sigma_clip(Halpha,Halphaerr,3)

    RApix=np.int64(hdr['CRPIX1'])
    DECpix=np.int64(hdr['CRPIX2'])
    Xnuc=hdr['NAXIS1']
    Ynuc=hdr['NAXIS2']
    Cell=np.abs(hdr['CD1_1'])

    Cell_arcsec=Cell*3600
    Cell_pc=4.84*Cell_arcsec*Dist[i]
    Cellcm=Cell_pc*3.086e18
    Cell_area=Cellcm**2

    imbeam=dist(Xnuc,Ynuc,beam[i]/3600,RApix,DECpix,Cell)

    Halphanuc=np.nansum(Halphamask_data*imbeam)*Cell_area

    SF=Halphanuc*5.5e-42
    SFR.append(SF)
print(SFR)