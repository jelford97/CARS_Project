import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Latin Modern Roman'
plt.rcParams.update({'font.size': 10})
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['xtick.labelsize'] = 12;
plt.rcParams['ytick.labelsize'] = 12
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
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['ytick.right']=True
plt.rcParams['xtick.top']=True


param=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/G_S_Param.csv')
data=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/Usable_Data.csv')
Maltang=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/MALATANG.csv')

Maltang_All=Maltang[(Maltang['HCN Detected']==1) & (Maltang['HCO Detected']==1)]
Maltang_HCO_ND=Maltang[Maltang['HCO Detected']==0]
Maltang_HCN_ND=Maltang[Maltang['HCN Detected']==0]

M_HCN=np.array(Maltang_All['L_HCN'])
E_M_HCN=np.array(Maltang_All['E_L_HCN'])
M_HCO=np.array(Maltang_All['L_HCO+'])
E_M_HCO=np.array(Maltang_All['E_L_HCO+'])
M_LIR=np.array(Maltang_All['L_IR'])
E_M_LIR=np.array(Maltang_All['E_L_IR'])

M_HCN_HCOND=np.array(Maltang_HCO_ND['L_HCN'])
E_M_HCN_HCOND=np.array(Maltang_HCO_ND['E_L_HCN'])
M_HCO_HCOND=np.array(Maltang_HCO_ND['L_HCO+'])
E_M_HCO_HCOND=np.array(Maltang_HCO_ND['E_L_HCO+'])
M_LIR_HCOND=np.array(Maltang_HCO_ND['L_IR'])
E_M_LIR_HCOND=np.array(Maltang_HCO_ND['E_L_IR'])

M_HCN_HCNND=np.array(Maltang_HCN_ND['L_HCN'])
E_M_HCN_HCNND=np.array(Maltang_HCN_ND['E_L_HCN'])
M_HCO_HCNND=np.array(Maltang_HCN_ND['L_HCO+'])
E_M_HCO_HCNND=np.array(Maltang_HCN_ND['E_L_HCO+'])
M_LIR_HCNND=np.array(Maltang_HCN_ND['L_IR'])
E_M_LIR_HCNND=np.array(Maltang_HCN_ND['E_L_IR'])

Galaxies=['HE0433','HE1029','HE1108']
SFR=np.array([19.4,27.1,12.4])
SFRerr=np.array([0.2,1,0.4])
NUC_SFR=np.array([0.12,5.89,0.16])
LIR=SFR/2e-10
LIR_err=SFRerr/2e-10
NUC_LIR=NUC_SFR/2e-10
Lines=['HCN','HCO']
z=np.array([0.035536,0.023953,0.040501])
H0=70
c=3e5
Dist=(c*z)/H0
Galaxy=[]
Line=[]
Intensity_K=[]
dist=[]
Lum=[]
Lum_error=[]
IR_Lum=[]
IR_Lum_err=[]
NUC_IR=[]
#Intensities are in Jy km/s as datacube units are Jy/beam
for i in range(len(Galaxies)):
    for j in range(len(Lines)):
        G_Data=data[data['Galaxy']==Galaxies[i]]
        L_Data=G_Data[G_Data['Line']==Lines[j]]
        Int=np.array(L_Data['Intensity (Jy km/s)'])
        G_Param=param[param['Galaxy']==Galaxies[i]]
        L_Param=G_Param[G_Param['Line']==Lines[j]]
        Freq=np.array(L_Param['Rest Freq (GHz)'])
        BMAJ=np.array(L_Param['Beam Width Major'])
        BMIN=np.array(L_Param['Beam Width Minor'])
        Error=np.array(L_Data['Error (Jy km/s)'])
        
        Int_mjy=Int*1e3 #Converts to mJy/beam
        Int_mjy_error=Error*1e3
        Beam=(np.pi*BMAJ*BMIN)/(4*np.log(2)) #Calculates the beam area
        Int_Beam=Int_mjy/Beam #Convert to mJy/beam 
        Int_Beam_error=Int_mjy_error/Beam
        QF=1.222e3*(1/((Freq**2)*BMAJ*BMIN)) #Calculates the conversion factor
        Int_K=Int_Beam*QF #Calculates the intensity in K km/s
        Int_K_error=Int_Beam_error*QF
        Beam_area=(BMAJ*4.83*Dist[i])*(BMIN*4.83*Dist[i]) #Calcualates the beam areas in pc^2
        LK=Int_K*Beam_area #Calculates the luminosity in K km/s pc^2
        LK_error=Int_K_error*Beam_area

        Galaxy.append(Galaxies[i])
        Line.append(Lines[j])
        Intensity_K.append(Int_K)
        Lum.append(int(LK))
        Lum_error.append(int(LK_error))
        IR_Lum.append(LIR[i])
        IR_Lum_err.append(int(LIR_err[i]))
        NUC_IR.append(NUC_LIR[i])


datadict={'Galaxy':np.array(Galaxy),'Line':np.array(Line),'Intensity (K km/s)':Intensity_K,'Luminosity (K km/s pc^2)':np.array(Lum,dtype=float),'Luminosity Error (K km/s pc^2)':np.array(Lum_error,dtype=float),'L_IR (L_solar)':np.array(IR_Lum,dtype=float),'L_IR Error (L_solar)':np.array(IR_Lum_err,dtype=float),'Nuclear L_IR':np.array(NUC_IR,dtype=float)}
DataDF=pd.DataFrame(datadict)

HCN_logspace=np.logspace(4,11)
HCO_logspace=np.logspace(4,11)


logIR_HCN=10**(1*np.log10(HCN_logspace)+3.80)
logIR_HCO=10**(1.13*np.log10(HCO_logspace)+2.83)



HCN=DataDF[DataDF['Line']=='HCN']
HCO=DataDF[DataDF['Line']=='HCO']

plt.loglog(HCN['Luminosity (K km/s pc^2)'],HCN['L_IR (L_solar)'],'o',zorder=2,color='orange',label='CARS')
plt.loglog(HCN['Luminosity (K km/s pc^2)'],HCN['Nuclear L_IR'],'o',zorder=2,color='green',label='CARS (Nuclear SFR)')
plt.loglog(M_HCN,M_LIR,'o',zorder=0,color='black')
plt.loglog(M_HCN_HCNND,M_LIR_HCNND,'<',color='black',zorder=0)
plt.loglog(M_HCN_HCOND,M_LIR_HCOND,'o',color='black',zorder=0)
plt.errorbar(M_HCN_HCNND,M_LIR_HCNND,xerr=E_M_HCN_HCNND,yerr=E_M_LIR_HCNND,fmt='None',ecolor='black',zorder=-1)
plt.errorbar(M_HCN_HCOND,M_LIR_HCOND,xerr=E_M_HCN_HCOND,yerr=E_M_LIR_HCOND,fmt='None',ecolor='black',zorder=-1)
plt.errorbar(HCN['Luminosity (K km/s pc^2)'],HCN['L_IR (L_solar)'],xerr=HCN['Luminosity Error (K km/s pc^2)'],yerr=HCN['L_IR Error (L_solar)'],fmt='None',ecolor='orange',zorder=1)
plt.errorbar(M_HCN,M_LIR,xerr=E_M_HCN,yerr=E_M_LIR,fmt='None',ecolor='black',zorder=-1)
#plt.loglog(MW_HCN,MW_LIR,'o',label='MW')
plt.plot(HCN_logspace,logIR_HCN,c='black',label='Tan+18',linestyle='--')
plt.xlabel('$log(L_{HCN (4-3)}) (K\,km\,s^{-1}\,pc^{2})$')
plt.ylabel('$log(L_{IR})\,(L_\odot)$')
plt.legend(frameon=False)
plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/HCN_SFR.png',bbox_inches='tight')
plt.close()

plt.loglog(HCO['Luminosity (K km/s pc^2)'],HCO['L_IR (L_solar)'],'o',zorder=2,color='orange',label='CARS')
plt.loglog(HCO['Luminosity (K km/s pc^2)'],HCO['Nuclear L_IR'],'o',zorder=2,color='green',label='CARS (Nuclear SFR)')
plt.loglog(M_HCO,M_LIR,'o',zorder=0,color='black')
plt.loglog(M_HCO_HCNND,M_LIR_HCNND,'o',color='black',zorder=0)
plt.loglog(M_HCO_HCOND,M_LIR_HCOND,'<',color='black',zorder=0)
plt.errorbar(M_HCO_HCNND,M_LIR_HCNND,xerr=E_M_HCO_HCNND,yerr=E_M_LIR_HCNND,fmt='None',ecolor='black',zorder=-1)
plt.errorbar(M_HCO_HCOND,M_LIR_HCOND,xerr=E_M_HCO_HCOND,yerr=E_M_LIR_HCOND,fmt='None',ecolor='black',zorder=-1)
plt.errorbar(HCO['Luminosity (K km/s pc^2)'],HCO['L_IR (L_solar)'],xerr=HCO['Luminosity Error (K km/s pc^2)'],yerr=HCO['L_IR Error (L_solar)'],fmt='None',ecolor='orange',zorder=1)
plt.errorbar(M_HCO,M_LIR,xerr=E_M_HCO,yerr=E_M_LIR,fmt='None',ecolor='black',zorder=-1)
plt.plot(HCO_logspace,logIR_HCO,c='black',label='Tan+18',linestyle='--')
plt.xlabel('$log(L_{HCO+ (4-3)}) (K\,km\,s^{-1}\,pc^{2})$')
plt.ylabel('$log(L_{IR}) \,(L_\odot)$')
plt.legend(frameon=False)
plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/HCO_SFR.png',bbox_inches='tight')
plt.close()