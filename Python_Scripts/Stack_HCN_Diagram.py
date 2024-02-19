from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

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

data=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/Usable_Data.csv')

IZ=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/Izumi.csv')
IZ_HR=IZ[IZ['High Res']==1]
IZ_HR_Dect=IZ_HR[IZ_HR['Detected']==1]
IZ_HR_ND=IZ_HR[IZ_HR['Detected']==0]
IZ_LR=IZ[IZ['Low Res']==1]


IZ_HR_AGN_D=IZ_HR_Dect[IZ_HR_Dect['Type']=='AGN']
IZ_HR_SB_D=IZ_HR_Dect[IZ_HR_Dect['Type']=='SB']

IZ_HR_AGN_ND=IZ_HR_ND[IZ_HR_ND['Type']=='AGN']
IZ_HR_SB_ND=IZ_HR_ND[IZ_HR_ND['Type']=='SB']


IZ_LR_AGN=IZ_LR[IZ_LR['Type']=='AGN']
IZ_LR_SB=IZ_LR[IZ_LR['Type']=='SB']
IZ_LR_BAGN=IZ_LR[IZ_LR['Type']=='B_AGN']

Zhang=pd.read_csv('/Users/jelford/Documents/PhD_Work/CARS_Project/CSV_Files/Zhang.csv')
Dect_Gal='HE1108'
Non_Dect_Gal=['HE0433','HE1029']

ZhangAGN=Zhang[Zhang['Type']=='AGN']
ZhangSF=Zhang[Zhang['Type']=='SF']

z_AGN_cs=np.array(ZhangAGN['I_CS'])
z_AGN_hcn=np.array(ZhangAGN['I_HCN'])
z_AGN_hco=np.array(ZhangAGN['I_HCO'])
z_AGN_e_hcn=np.array(ZhangAGN['E_I_HCN'])
z_AGN_e_hco=np.array(ZhangAGN['E_I_HCO'])

Z_AGN_HCN_HCO_up=[]
Z_AGN_HCN_HCO_low=[]
for ii in range(len(z_AGN_hcn)):
    Z_AGN_HCN_HCO_err=(z_AGN_hcn[ii]+np.random.normal(0,z_AGN_e_hcn[ii],1000))/(z_AGN_hco[ii]+np.random.normal(0,z_AGN_e_hco[ii],1000))
    Z_AGN_HCN_HCO_lower=np.percentile(Z_AGN_HCN_HCO_err,16)
    Z_AGN_HCN_HCO_upper=np.percentile(Z_AGN_HCN_HCO_err,84)
    Z_AGN_HCN_HCO_up.append(Z_AGN_HCN_HCO_upper)
    Z_AGN_HCN_HCO_low.append(Z_AGN_HCN_HCO_lower)

z_SF_cs=np.array(ZhangSF['I_CS'])
z_SF_hcn=np.array(ZhangSF['I_HCN'])
z_SF_hco=np.array(ZhangSF['I_HCO'])
z_SF_e_hcn=np.array(ZhangSF['E_I_HCN'])
z_SF_e_hco=np.array(ZhangSF['E_I_HCO'])

Z_SF_HCN_HCO_up=[]
Z_SF_HCN_HCO_low=[]
for jj in range(len(z_SF_hcn)):
    Z_SF_HCN_HCO_err=(z_SF_hcn[jj]+np.random.normal(0,z_SF_e_hcn[jj],1000))/(z_SF_hco[jj]+np.random.normal(0,z_SF_e_hco[jj],1000))
    Z_SF_HCN_HCO_lower=np.percentile(Z_SF_HCN_HCO_err,16)
    Z_SF_HCN_HCO_upper=np.percentile(Z_SF_HCN_HCO_err,84)
    Z_SF_HCN_HCO_up.append(Z_SF_HCN_HCO_upper)
    Z_SF_HCN_HCO_low.append(Z_SF_HCN_HCO_lower)



#Z_AGN_HCN_HCO_err=(z_AGN_hcn+np.random.normal(0,z_AGN_e_hcn,1000))/(z_AGN_hco+np.random.normal(0,z_AGN_e_hco,1000))
#Z_AGN_HCN_HCO_lower=np.percentile(Z_AGN_HCN_HCO_err,16)
#Z_AGN_HCN_HCO_upper=np.percentile(Z_AGN_HCN_HCO_err,84)

#Z_SF_HCN_HCO_err=(z_SF_hcn+np.random.normal(0,z_SF_e_hcn,1000))/(z_SF_hco+np.random.normal(0,z_SF_e_hco,1000))
#Z_SF_HCN_HCO_lower=np.percentile(Z_SF_HCN_HCO_err,16)
#Z_SF_HCN_HCO_upper=np.percentile(Z_SF_HCN_HCO_err,84)

Dect_Data=data[data['Galaxy']==Dect_Gal]

CS_Dect_data=Dect_Data[Dect_Data['Line']=='CS']
CS_Dect_Int=np.array(CS_Dect_data['Intensity (Jy km/s)'])
#print(CS_Dect_Int)
CS_Dect_Err=np.array(CS_Dect_data['Error (Jy km/s)'])

HCN_Dect_data=Dect_Data[Dect_Data['Line']=='HCN']
HCN_Dect_Int=np.array(HCN_Dect_data['Intensity (Jy km/s)'])
#print(HCN_Dect_Int)
HCN_Dect_Err=np.array(HCN_Dect_data['Error (Jy km/s)'])

HCO_Dect_data=Dect_Data[Dect_Data['Line']=='HCO']
HCO_Dect_Int=np.array(HCO_Dect_data['Intensity (Jy km/s)'])
HCO_Dect_Err=np.array(HCO_Dect_data['Error (Jy km/s)'])

HCN_CS_Dect=HCN_Dect_Int/CS_Dect_Int
HCN_HCO_Dect=HCN_Dect_Int/HCO_Dect_Int

HCN_CS_err=(HCN_Dect_Int+np.random.normal(0,HCN_Dect_Err,1000))/(CS_Dect_Int+np.random.normal(0,CS_Dect_Err,1000))
HCN_CS_lower=np.percentile(HCN_CS_err,16)
HCN_CS_upper=np.percentile(HCN_CS_err,84)

HCN_HCO_err=(HCN_Dect_Int+np.random.normal(0,HCN_Dect_Err,1000))/(HCO_Dect_Int+np.random.normal(0,HCO_Dect_Err,1000))
HCN_HCO_lower=np.percentile(HCN_HCO_err,16)
HCN_HCO_upper=np.percentile(HCN_HCO_err,84)


HCN_CS_A=[]
HCN_HCO_A=[]
HCN_HCO_ND_low=[]
HCN_HCO_ND_up=[]
for i in range(len(Non_Dect_Gal)):
    Non_Dect_Data=data[data['Galaxy']==Non_Dect_Gal[i]]

    CS_Non_Dect_data=Non_Dect_Data[Non_Dect_Data['Line']=='CS']
    CS_Non_Dect_Int=np.array(CS_Non_Dect_data['Intensity (Jy km/s)'])

    HCN_Non_Dect_data=Non_Dect_Data[Non_Dect_Data['Line']=='HCN']
    HCN_Non_Dect_Int=np.array(HCN_Non_Dect_data['Intensity (Jy km/s)'])
    HCN_Non_Dect_Err=np.array(HCN_Non_Dect_data['Error (Jy km/s)'])

    HCO_Non_Dect_data=Non_Dect_Data[Non_Dect_Data['Line']=='HCO']
    HCO_Non_Dect_Int=np.array(HCO_Non_Dect_data['Intensity (Jy km/s)'])
    HCO_Non_Dect_Err=np.array(HCO_Non_Dect_data['Error (Jy km/s)'])


    HCN_CS_Non_Dect=HCN_Non_Dect_Int/CS_Non_Dect_Int
    HCN_CS_A.append(HCN_CS_Non_Dect)
    HCN_HCO_Non_Dect=HCN_Non_Dect_Int/HCO_Non_Dect_Int
    HCN_HCO_A.append(HCN_HCO_Non_Dect)

    HCN_HCO_NonDect_err=(HCN_Non_Dect_Int+np.random.normal(0,HCN_Non_Dect_Err,1000))/(HCO_Non_Dect_Int+np.random.normal(0,HCO_Non_Dect_Err,1000))
    HCN_HCO_ND_lower=np.percentile(HCN_HCO_NonDect_err,16)
    HCN_HCO_ND_upper=np.percentile(HCN_HCO_NonDect_err,84)
    HCN_HCO_ND_low.append(HCN_HCO_ND_lower)
    HCN_HCO_ND_up.append(HCN_HCO_ND_upper)


#print(HCN_CS_Dect)
#print(HCN_HCO_Dect)

#print(HCN_CS_upper)
#print(HCN_CS_lower)

#print(HCN_HCO_upper)
#print(HCN_HCO_lower)

plt.plot(IZ_HR_AGN_D['HCN/HCO'],IZ_HR_AGN_D['HCN/CS'],'o',color='red',label='Izumi AGN')
plt.plot(IZ_HR_SB_D['HCN/HCO'],IZ_HR_SB_D['HCN/CS'],'o',color='blue',label='Izumi Starburst')
plt.plot(IZ_HR_AGN_ND['HCN/HCO'],IZ_HR_AGN_ND['HCN/CS'],'^',color='red')
plt.plot(IZ_HR_SB_ND['HCN/HCO'],IZ_HR_SB_ND['HCN/CS'],'^',color='blue')
plt.plot(IZ_LR_AGN['HCN/HCO'],IZ_LR_AGN['HCN/CS'],'o',fillstyle='none',color='red')
plt.plot(IZ_LR_SB['HCN/HCO'],IZ_LR_SB['HCN/CS'],'o',fillstyle='none',color='blue')
plt.plot(IZ_LR_BAGN['HCN/HCO'],IZ_LR_BAGN['HCN/CS'],'o',fillstyle='none',color='green',label='Izumi Buried AGN')
plt.plot((z_AGN_hcn/z_AGN_hco),(z_AGN_hcn/z_AGN_cs),'^',fillstyle='none',color='pink',label='Zhang AGN')
plt.plot((z_SF_hcn/z_SF_hco),(z_SF_hcn/z_SF_cs),'^',fillstyle='none',color='black',label='Zhang SF')
plt.plot(HCN_HCO_Dect,HCN_CS_Dect,'o',color='orange',zorder=3)
plt.plot(HCN_HCO_A,HCN_CS_A,'^',color='orange',zorder=3)
plt.hlines((z_AGN_hcn/z_AGN_cs),Z_AGN_HCN_HCO_up,Z_AGN_HCN_HCO_low,color='pink')
plt.hlines((z_SF_hcn/z_SF_cs),Z_SF_HCN_HCO_up,Z_SF_HCN_HCO_low,color='black')
plt.hlines(HCN_CS_Dect,HCN_HCO_upper,HCN_HCO_lower,color='orange')
plt.vlines(HCN_HCO_Dect,HCN_CS_upper,HCN_CS_lower,color='orange')
plt.hlines(HCN_CS_A,HCN_HCO_ND_up,HCN_HCO_ND_low,color='orange')
plt.errorbar(IZ_HR_AGN_D['HCN/HCO'],IZ_HR_AGN_D['HCN/CS'],xerr=IZ_HR_AGN_D['Error1'],yerr=IZ_HR_AGN_D['Error2'],fmt='None',ecolor='red')
plt.errorbar(IZ_HR_SB_D['HCN/HCO'],IZ_HR_SB_D['HCN/CS'],IZ_HR_SB_D['Error1'],IZ_HR_SB_D['Error2'],fmt='None',ecolor='blue')
plt.errorbar(IZ_HR_AGN_ND['HCN/HCO'],IZ_HR_AGN_ND['HCN/CS'],xerr=IZ_HR_AGN_ND['Error1'],yerr=IZ_HR_AGN_ND['Error2'],fmt='None',ecolor='red')
plt.errorbar(IZ_HR_SB_ND['HCN/HCO'],IZ_HR_SB_ND['HCN/CS'],IZ_HR_SB_ND['Error1'],IZ_HR_SB_ND['Error2'],fmt='None',ecolor='blue')
plt.errorbar(IZ_LR_AGN['HCN/HCO'],IZ_LR_AGN['HCN/CS'],xerr=IZ_LR_AGN['Error1'],yerr=IZ_LR_AGN['Error2'],fmt='None',ecolor='red')
plt.errorbar(IZ_LR_SB['HCN/HCO'],IZ_LR_SB['HCN/CS'],IZ_LR_SB['Error1'],IZ_LR_SB['Error2'],fmt='None',ecolor='blue')
plt.errorbar(IZ_LR_BAGN['HCN/HCO'],IZ_LR_BAGN['HCN/CS'],xerr=IZ_LR_BAGN['Error1'],yerr=IZ_LR_BAGN['Error2'],fmt='None',ecolor='green')
plt.ylabel('HCN(4-3)/CS(7-6)')
plt.xlabel('HCN(4-3)/HCO$^+$(4-3)')
plt.legend(loc='upper left',frameon=False)
plt.savefig('/Users/jelford/Documents/PhD_Work/CARS_Project/Plots/HCN_diagram.png')
plt.close()

