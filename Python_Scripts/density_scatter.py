import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from astropy.io import fits
import pandas as pd

plt.rcParams['font.family'] = 'Latin Modern Roman'
plt.rcParams.update({'font.size': 10})
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['xtick.labelsize'] = 10;
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['xtick.major.size'] = 10;
plt.rcParams['ytick.major.size'] = 10
plt.rcParams['xtick.major.width'] = 2;
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['xtick.minor.size'] = 5;
plt.rcParams['ytick.minor.size'] = 5
plt.rcParams['xtick.minor.width'] = 1;
plt.rcParams['ytick.minor.width'] = 1
plt.rcParams['xtick.direction'] = 'in';
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.bottom'] = True
plt.rcParams['ytick.left'] = True
params = {'mathtext.default': 'regular'}
plt.rcParams.update(params)
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['ytick.right']=True
plt.rcParams['xtick.top']=True

Galaxy_maps=['HE0108-4743','HE0433-1028','HE1353-1917','HE1108-2813','HE1029-1831']
Galaxy_abr=['HE0108','HE0433','HE1353','HE1108','HE1029']
beam=[0.78,1.03,0.77,1.00,0.82]

def sigma_clip(data,err,fac):
    sn=data/err
    mask=np.where(sn>fac,1,np.NaN)
    mask_data=data*mask
    return mask_data

for i in range(len(Galaxy_maps)):
    hdu=fits.open('/Users/jelford/Documents/PhD_Work/CARS_Data/'+str(Galaxy_abr[i])+'/'+str(Galaxy_maps[i])+'.MUSE.WFM-NOAO.maps-full.fits')
    OIII=hdu[11].data
    hdr=hdu[11].header
    OIIIerr=hdu[12].data
    OIIImask_data=sigma_clip(OIII,OIIIerr,3)

    Hbeta=hdu[13].data
    Hbetaerr=hdu[14].data
    Hbetamask_data=sigma_clip(Hbeta,Hbetaerr,3)

    NII=hdu[23].data
    NIIerr=hdu[24].data
    NIImask_data=sigma_clip(NII,NIIerr,3)

    Halpha=hdu[9].data
    Halphaerr=hdu[10].data
    Halphamask_data=sigma_clip(Halpha,Halphaerr,3)

    SII=hdu[25].data
    SIIerr=hdu[26].data
    SIImask_data=sigma_clip(SII,SIIerr,3)

    OI=hdu[19].data
    OIerr=hdu[20].data
    OImask_data=sigma_clip(OI,OIerr,3)

    map_shape=OIII.shape
    shape=map_shape[0]*map_shape[1]

    BPT_x=(NIImask_data/Halphamask_data).reshape(shape)
    VO_SIIx=(SIImask_data/Halphamask_data).reshape(shape)
    VO_OIx=(OImask_data/Halphamask_data).reshape(shape)

    y=(OIIImask_data/Hbetamask_data).reshape(shape)

    #Nuclear
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
    
    RApix=np.int64(hdr['CRPIX1'])
    DECpix=np.int64(hdr['CRPIX2'])
    Xnuc=hdr['NAXIS1']
    Ynuc=hdr['NAXIS2']
    Cell=np.abs(hdr['CD1_1'])

    imbeam=dist(Xnuc,Ynuc,beam[i]/3600,RApix,DECpix,Cell)
    
    OIIInuc=OIIImask_data*imbeam
    Hbetanuc=Hbetamask_data*imbeam
    NIInuc=NIImask_data*imbeam
    Halphanuc=Halphamask_data*imbeam
    SIInuc=SIImask_data*imbeam
    OInuc=OImask_data*imbeam

    BPT_nuc=(NIInuc/Halphanuc).reshape(shape)
    VO_SII_nuc=(SIInuc/Halphanuc).reshape(shape)
    VO_OI_nuc=(OInuc/Halphanuc).reshape(shape)

    y_nuc=(OIIInuc/Hbetanuc).reshape(shape)

    #BPT Diagram
    XK1=np.linspace(-1.5,0.3)
    YK1=(0.61/(XK1-0.47))+1.19

    XS7=np.linspace(-0.180,1.5)
    YS7=1.05*XS7+0.45

    XK3=np.linspace(-1.5,0.)
    YK3=0.61/(XK3-0.05)+1.3

    #VO87-SII Diagram
    XAGN=np.linspace(-1.5,0.3)
    YAGN=0.72/(XAGN-0.32)+1.30

    XLINER=np.linspace(-0.30,1.5)
    YLINER=1.89*XLINER+0.76

    #VO87-OI
    XAGN2=np.linspace(-2,0.3)
    YAGN2=0.73/(XAGN2-0.32)+1.33

    XLINER2=np.linspace(-0.6,1.5)
    YLINER2=1.18*XLINER2+1.30

    BPTdict={'x':BPT_x,'y':y}
    BPTDF=pd.DataFrame(BPTdict)
    BPTDF_NoN=BPTDF.dropna()
    BPT_x_NoN=BPTDF_NoN['x']
    y_NoN_BPT=BPTDF_NoN['y']
    
    xy_bpt=np.vstack([BPT_x_NoN,y_NoN_BPT])
    z_bpt=gaussian_kde(xy_bpt)(xy_bpt)
    
    plt.scatter(np.log10(BPT_x_NoN),np.log10(y_NoN_BPT),c=z_bpt,s=100,label='Global')
    plt.plot(np.log10(BPT_nuc),np.log10(y_nuc),'o',color='red',label='Nuclear',markersize=2)
    plt.plot(XK1,YK1,'--',color='black')
    plt.plot(XS7,YS7,'--',color='black')
    plt.plot(XK3,YK3,'--',color='black')
    plt.xlabel(r"log([NII] $\lambda$ 6583/H$\alpha$)")
    plt.ylabel(r"log([OIII] $\lambda$ 5007/H$\beta$)")
    plt.text(-1,1,'AGN')
    plt.text(0.5,0,'LINER')
    plt.text(-0.2,-1,'Comp')
    plt.text(-1,-1,'HII')
    plt.xlim(-1.2,1.2)
    plt.ylim(-1.5,1.5)
    plt.legend(loc='upper right')

    plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/'+str(Galaxy_abr[i])+'/'+str(Galaxy_abr[i])+'BPT_DS.png')
    plt.close()

    VO_SIIdict={'x':VO_SIIx,'y':y}
    VOSIIDF=pd.DataFrame(VO_SIIdict)
    VOSIIDF_NoN=VOSIIDF.dropna()
    VOSII_x_NoN=VOSIIDF_NoN['x']
    y_NoN_VOSII=VOSIIDF_NoN['y']

    xy_VO_SII=np.vstack([VOSII_x_NoN,y_NoN_VOSII])
    z_VO_SII=gaussian_kde(xy_VO_SII)(xy_VO_SII)

    plt.scatter(np.log10(VOSII_x_NoN),np.log10(y_NoN_VOSII),c=z_VO_SII,s=100,label='Global')
    plt.plot(np.log10(VO_SII_nuc),np.log10(y_nuc),'o',color='red',label='Nuclear',markersize=2)
    plt.plot(XAGN,YAGN,'--',color='black')
    plt.plot(XLINER,YLINER,'--',color='black')
    plt.xlabel(r"log([SII] $\lambda$ 6717/H$\alpha$)")
    plt.ylabel(r"log([OIII] $\lambda$ 5007/H$\beta$)")
    plt.text(-1,1.2,'Seyfert')
    plt.text(0.5,-0.5,'LINER')
    plt.text(-1.2,-1.2,'HII')
    plt.xlim(-1.5,1.2)
    plt.ylim(-1.5,1.5)
    plt.legend(loc='upper right')

    plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/'+str(Galaxy_abr[i])+'/'+str(Galaxy_abr[i])+'V087-SII_DS.png')
    plt.close()

    VOOIdict={'x':VO_OIx,'y':y}
    VOOIDF=pd.DataFrame(VOOIdict)
    VOOIDF_NoN=VOOIDF.dropna()
    VOOI_x_NoN=VOOIDF_NoN['x']
    y_NoN_VOOI=VOOIDF_NoN['y']

    xy_VO_OI=np.vstack([VOOI_x_NoN,y_NoN_VOOI])
    z_VO_OI=gaussian_kde(xy_VO_OI)(xy_VO_OI)
    
    plt.scatter(np.log10(VOOI_x_NoN),np.log10(y_NoN_VOOI),s=100,c=z_VO_OI,label='Global')
    plt.plot(np.log10(VO_OI_nuc),np.log10(y_nuc),'o',color='red',label='Nuclear',markersize=2)
    plt.plot(XAGN2,YAGN2,'--',color='black')
    plt.plot(XLINER2,YLINER2,'--',color='black')
    plt.xlabel(r"log([OI] $\lambda$ 6300/H$\alpha$)")
    plt.ylabel(r"log([OIII] $\lambda$ 5007/H$\beta$)")
    plt.text(-1,1.2,'Seyfert')
    plt.text(0.7,0,'LINER')
    plt.text(-1,-1.2,'HII')
    plt.xlim(-2,1.2)
    plt.ylim(-1.5,1.5)
    plt.legend(loc='upper right')

    plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/'+str(Galaxy_abr[i])+'/'+str(Galaxy_abr[i])+'V087-OI_DS.png')
    plt.close()
