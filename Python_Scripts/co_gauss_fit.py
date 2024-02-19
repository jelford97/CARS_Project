import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gastimator import gastimator

def gauss(params,x):
    A1, x01, sigma1,base= params[0],params[1],params[2],params[3]
    return (A1 * np.exp(-(x - x01) ** 2 / (2 * sigma1 ** 2)))  + base



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

data=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Data/HE1108/HE1108-2813_spec.csv')
vout=data['Velocity (km/s)']-10103
outspec=data['Flux Density (mJy)']
outrms=np.full(len(outspec),0.46)

Gauss_Fit=fit_single(vout,outspec,outrms)
print(Gauss_Fit[0])
Gauss_plot=gauss(Gauss_Fit[0],vout)
plt.step(vout,outspec)
plt.plot(vout,Gauss_plot)
plt.show()

file=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Data/HE0433/HE0433-1028_specmask.csv')
file1=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Data/HE1108/HE1108-2813_specmask.csv')
file2=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Data/HE1353/HE1353-1917_specmask.csv')

HE0433I=np.sum(file['Flux Density (mJy)'])*20*1e-3
HE1108I=np.sum(file1['Flux Density (mJy)'])*20*1e-3
HE1353I=np.sum(file2['Flux Density (mJy)'])*20*1e-3

HE0433Ierr=np.sqrt(len(file['Flux Density (mJy)']))*4.64e-4*20
HE1108Ierr=np.sqrt(len(file1['Flux Density (mJy)']))*8.59e-4*20
HE1353Ierr=np.sqrt(len(file2['Flux Density (mJy)']))*3.70e-4*20

print(HE0433I)
print(HE0433Ierr)
print(HE1108I)
print(HE1108Ierr)
print(HE1353I)
print(HE1353Ierr)