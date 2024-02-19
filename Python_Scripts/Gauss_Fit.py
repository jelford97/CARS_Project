from gastimator import gastimator
import numpy as np
import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt

def gauss(params,x):
    A, x0, sigma,base = params[0],params[1],params[2],params[3]
    return A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))  + base



def fit_single(vouta,spectruma,spectrum_errora,impose=[]):
    mcmc = gastimator(gauss,vouta)
    mcmc.labels=np.array(['Peak1','centre1','sigma1','baseline'])
    mcmc.min=np.array([0.,-130.,0,-0.2])
    mcmc.max=np.array([np.max(spectruma)*2,130, 50,0.2])
    mcmc.fixed=np.array([False, False,False,False])
    if len(impose) > 0:
        mcmc.guesses =impose[:-1]
        mcmc.fixed[1]=True
        mcmc.guesses[0]=np.max(spectruma)*0.9
        mcmc.max[2]=impose[2]
        #mcmc.fixed=np.array([False, True,True,False])
    else:
        mcmc.guesses=np.array([np.max(spectruma)*0.9,np.clip(np.sum(spectruma*vouta)/np.sum(spectruma),mcmc.min[1],mcmc.max[1]),15,0])




    mcmc.precision=np.array([np.max(spectruma)*0.3,3.,5.,0.1])
    mcmc.silent=True
    outputvalue, outputll= mcmc.run(spectruma,spectrum_errora,10000,plot=False,nchains=3)
    bestfit=np.median(outputvalue,axis=1)
    errs=np.std(outputvalue,axis=1)
    totflux = ((outputvalue[0,:] * outputvalue[2,:])) * np.sqrt(2*np.pi)
    bestfit=np.append(bestfit,np.median(totflux))
    #breakpoint()
    errs=np.append(errs,np.std(totflux))


    bic=4*np.log(spectruma.size) - 2*np.max(outputll)
    return bestfit, errs, bic,outputvalue

Non_Dect_param=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/Non_Dect_Param.csv')
Dect_Param=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/Dect_Param.csv')

Non_Dect_Path=np.array(Non_Dect_param['File Path'])
Vel_Min=np.array(Non_Dect_param['Line Vel Min'])
Vel_Max=np.array(Non_Dect_param['Line Vel Max'])
Line_W=np.array(Non_Dect_param['Line Width'])


Galaxy=np.array(Dect_Param['Galaxy'])
Line=np.array(Dect_Param['Line'])
Dect_Path=np.array(Dect_Param['File Path'])
Beam=np.array(Dect_Param['Beam'])

Dect_T_Int_A=[]
Dect_T_rms_int=[]

for i in range(len(Dect_Path)):
    hdu=fits.open(Dect_Path[i])
    data=hdu[0].data

    vout=data[:,0]
    outspec=data[:,1]
    outrms=data[:,2]

    Gauss_Fit=fit_single(vout,outspec,outrms)
    B_Fit=Gauss_Fit[0]
    T_Flux=B_Fit[4]
    T_Int=T_Flux*Beam[i]
    Dect_T_Int_A.append(T_Int)
    Errors=Gauss_Fit[1]
    rms=Errors[4]*Beam[i]
    Dect_T_rms_int.append(rms)
        
    Gauss_plot=gauss(Gauss_Fit[0],vout)
    plt.step(vout,outspec)
    plt.plot(vout,Gauss_plot)
    # toplot=np.random.choice(np.arange(Gauss_Fit[3].shape[1]),size=100)
    # for k in toplot:
    #         Gauss_plot=gauss(Gauss_Fit[3][:,k],vout)
    #         plt.plot(vout,Gauss_plot,alpha=0.1,color='k')
    plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/Gauss_Fit/Gauss'+str(Galaxy[i])+str(Line[i])+'_spectra.png',bbox_inches='tight')
    plt.close()

Non_Dect_Int_A=[]
Non_Dect_RMS_Flux=[]
for j in range(len(Non_Dect_Path)):
    hdu=fits.open(Non_Dect_Path[j])
    data=hdu[0].data

    vout=(data[:,0]).astype(int)
    outrms=data[:,2]
    outn=data[:,3]
        
    Vel_Min_I=int(Vel_Min[j])
    Vel_Max_I=int(Vel_Max[j])
        
    c=np.where(vout==Vel_Min_I)
    d=np.where(vout==Vel_Max_I)
    
    ci=int(c[0])
    di=int(d[0])

    non_dect_rms=outrms[ci:di]
    non_dectn=outn[ci:di]
    non_dect=non_dect_rms/(np.sqrt(non_dectn))

    med_sig=np.median(non_dect)

    T_Flux=3*med_sig
    Non_Dect_RMS_Flux.append(T_Flux)
    T_Int=T_Flux*Line_W[j]
    Non_Dect_Int_A.append(T_Int)



 

Dect_Param['Intensity (Jy km/s)']=Dect_T_Int_A
Dect_Param['Error (Jy km/s)']=Dect_T_rms_int
Dect_Param.to_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/Dect_Param.csv',index=False)

Non_Dect_param['Upper Limit Flux (Jy)']=Non_Dect_RMS_Flux
Non_Dect_param['Upper Limit Intensity (Jy km/s)']=Non_Dect_Int_A
Non_Dect_param.to_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/Non_Dect_Param.csv',index=False)