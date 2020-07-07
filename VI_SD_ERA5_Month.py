# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:06:25 2019

@author: guillaume
"""
import netCDF4
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pylab as plt
import warnings; warnings.filterwarnings(action='once')
import seaborn as sns
from matplotlib import gridspec
import xarray as xr


list_mon = range(1,5)
df = []
for yi in range(1982,2020,1):
    filename= 'J:/REANALYSES/ERA5/SWE_Cumul_Nittasinan/ERA5_Cumul_MONTH_SWE_'+str(yi)+'.nc' 
    sd_dataset = xr.open_mfdataset(filename)
    df2 = sd_dataset.sd.mean(dim=('longitude','latitude')).to_dataframe("SD").dropna(how='all')  
    df2.reindex([11, 12, 1,2,3])   
   # df2 = pd.DataFrame(df2.SD.cumsum())
    df2 = pd.DataFrame(df2)
    
    df2['date'] = pd.date_range(start='11/1/'+str(yi-1), end='3/1/'+str(yi), freq='MS')  
    df2['mois'] = df2['date'].dt.month
    df2['annee'] = df2['date'].dt.year
    
    df.append(df2)
    
df = pd.concat(df)
months_in_order = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar']
months_in_order = [11, 12, 1, 2, 3]
df3 = df.pivot(index='annee', columns='mois', values='SD')
df3 = df3.rename(columns={1: "Janvier", 2: "Février", 3: "Mars", 11: "Novembre",12: "Décembre"})

ax = plt.axes()
ax = df3.plot(kind='bar', figsize=(17, 10), color=['red', 'blue', 'green','yellow', 'orange'], rot=90, width=1.0)  
                                     
plt.title("Épaisseur total de la neige sur Pessamit", y=1.013,fontsize=30)
plt.xlabel("Années", labelpad=16,fontsize=30)
plt.ylabel("Épaisseur de neige [m]", labelpad=16,fontsize=30);
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(20)
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(20)
    
figure = ax.get_figure()    
figure.set_size_inches(22, 15) 
plt.savefig('./Cumul_Neige_Pessamit_timeserie_1981-2019.png', bbox_inches='tight', pad_inches=0.1)
plt.show()





