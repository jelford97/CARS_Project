import numpy as np

dense_LSB=np.array([1.22e-4,7.66e-4,8.25e-4,8.84e-4])
dense_USB=np.array([2.12e-4,7.44e-4,9.90e-4,1.13e-3])
dense_LSB_freq=np.array([3.35e11,3.31e11,3.30e11,3.35e11])
dense_USB_freq=np.array([3.47e11,3.43e11,3.41e11,3.47e11])

CO_LSB=np.array([1.70e-4,1.16e-4,4.40e-5])
CO_USB=np.array([2.17e-4,1.19e-4,6.65e-5])
CO_LSB_freq=np.array([9.83e10,9.94e10,9.83e10])
CO_USB_freq=np.array([1.10e11,1.11e11,1.10e11])
#dense_LSB_error=np.array([])
#dense_USB_error=np.array([])


def index(ALMAfreq,ALMA):
    lalma=np.log10(ALMA)
    lalmafreq=np.log10(ALMAfreq)
    m=(lalma[1]-lalma[0])/(lalmafreq[1]-lalmafreq[0])
    return m


    merr=np.abs(m)*np.sqrt(((dx/x)**2)+((dy/y)**2))
    return merr

for i in range(len(dense_LSB)):
    Flux=np.array([dense_LSB[i],dense_USB[i]])
    ALMA_Freq=np.array([dense_LSB_freq[i],dense_USB_freq[i]])
    SI=index(ALMA_Freq,Flux)
    print(SI)

print()
for j in range(len(CO_LSB)):
    Flux_CO=np.array([CO_LSB[j],CO_USB[j]])
    ALMA_Freq_CO=np.array([CO_LSB_freq[j],CO_USB_freq[j]])
    SI_CO=index(ALMA_Freq_CO,Flux_CO)
    print(SI_CO)