import matplotlib
matplotlib.use('TKAgg')
import numpy as np
import matplotlib.pylab as plt
from PyAstronomy.pyTiming import pyPDM
import pandas as pd


df = pd.read_csv(filepath_or_buffer='01344188+3053275.csv')

#print (df)
S= pyPDM.Scanner(minVal=100,maxVal=1200,dVal=1,mode="period")

col_list = list(set(df['filter'].tolist()))

#print(col_list)

fig,axs=plt.subplots(3,1,figsize=(8,10))
fig.subplots_adjust(hspace=0.4)

f_total=1
t_total=1
for data_filter in col_list:
    #print (data_filter)
    MJD=np.array( df['MJD'][df['filter']==data_filter].tolist())
    mag=np.array( df['mag'][df['filter']==data_filter].tolist())
    error=np.array( df['error'][df['filter']==data_filter].tolist())
    #print (MJD,mag)
    P_filter=pyPDM.PyPDM(MJD,mag)
    f,t =  P_filter.pdmEquiBinCover(10,4,S)
    #print (f,t)
    axs[0].plot(f, t)
    f_total=f
    t_total=t_total*t

axs[1].plot(f_total,t_total)

best_period=f_total[t_total== np.min(t_total)]

for data_filter in col_list:
    #print (data_filter)
    MJD=np.array( df['MJD'][df['filter']==data_filter].tolist())
    mag=np.array( df['mag'][df['filter']==data_filter].tolist())
    error=np.array( df['error'][df['filter']==data_filter].tolist())
    phase=np.array( df['MJD'][df['filter']==data_filter].tolist())/best_period - np.array( df['MJD'][df['filter']==data_filter].tolist())//best_period
    axs[2].errorbar(phase,mag,error,fmt='.')
sizef=17
axs[1].set_xlabel("period",fontsize=sizef)
axs[0].set_ylabel("Theta",fontsize=sizef)
axs[1].set_ylabel("Theta",fontsize=sizef)
axs[2].set_xlabel("Phase",fontsize=sizef)
axs[2].set_ylabel("Mag",fontsize=sizef)
axs[2].invert_yaxis()
plt.show()
