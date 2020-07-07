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
import gc

# ouverture du masque
mask = xr.open_mfdataset('nitassinan_CORDEX.nc')

rep1='K:/PROJETS/PROJET_CORDEX/CORDEX-NAM44/DRY_INDICES/'
variable_in = 'DC'

list_rcp85 = ['CANRCM4_NAM-44_ll_CanESM2_rcp85',            
              'HIRHAM5_NAM-44_ll_ICHEC-EC-EARTH_rcp85',  
              'RCA4.v1_NAM-44_ll_CCCma-CanESM2_rcp85','RCA4.v1_NAM-44_ll_ICHEC-EC-EARTH_rcp85',
              'RegCM4_NAM-44_ll_MPI-ESM-LR_rcp85','RegCM4_NAM-44_ll_GFDL-ESM2M_rcp85']

list_histo = ['CANRCM4_NAM-44_ll_CanESM2_historical',             
              'HIRHAM5_NAM-44_ll_ICHEC-EC-EARTH_histo',  
              'RCA4.v1_NAM-44_ll_CCCma-CanESM2_histo','RCA4.v1_NAM-44_ll_ICHEC-EC-EARTH_histo',
              'RegCM4_NAM-44_ll_MPI-ESM-LR_histo','RegCM4_NAM-44_ll_GFDL-ESM2M_histo']

df_rcp85 = []
for i in range(0,len(list_rcp85)): 
    df= []
    for yi in range(2010,2099,1):
        gc.collect()  
        filename= rep1 + list_rcp85[i] + '/'  + variable_in + '/' +  list_rcp85[i] +  '_Month_Mean_DC_' 
        multi_file = ([f'{filename}{yi}_from_4_to_8.nc' ])        
        ds_in = xr.open_mfdataset(multi_file)  
        ds_in = ds_in.rename({'x': 'y','y': 'x'})        
        ds_in = ds_in.DC.where(mask.DC >= 0)
        df2 = ds_in.max(dim=('x','y')).to_dataframe('DC'+str(i)).dropna(how='all')         
        df2 = pd.DataFrame(df2)       
        df.append(df2)
    df_rcp85.append(pd.concat(df))  
    
df_rcp85 = pd.concat(df_rcp85,axis=1)        
        #ds_in.plot()
         
       

df_histo = []
for i in range(0,len(list_histo)): 
    df= []
    for yi in range(1971,2001,1):
        gc.collect()  
        filename= rep1 + list_histo[i] + '/'  + variable_in + '/' +  list_histo[i] +  '_Month_Mean_DC_' 
        multi_file = ([f'{filename}{yi}_from_4_to_8.nc' ])        
        ds_in = xr.open_mfdataset(multi_file)  
        ds_in = ds_in.rename({'x': 'y','y': 'x'})        
        ds_in = ds_in.DC.where(mask.DC >= 0)
        df2 = ds_in.max(dim=('x','y')).to_dataframe('DC'+str(i)).dropna(how='all')         
        df2 = pd.DataFrame(df2)       
        df.append(df2)
    df_histo.append(pd.concat(df))  
    
df_histo = pd.concat(df_histo,axis=1)  
 
df1 = df_histo.apply(np.mean, axis=1)
df2 = df_rcp85.apply(np.mean, axis=1)

result = pd.DataFrame(pd.concat([df1, df2]),columns = ['DC'])
result =  result.resample('M').mean()
result['month'] = result.index.strftime("%b")

color = ['blue', 'red','green','orange','black']
fig = plt.figure(figsize=(22, 12)) 
gs = gridspec.GridSpec(1, 2, width_ratios=[6, 1]) 
gs.update( wspace=0.04)
ax1 = plt.subplot(gs[0])

plt.rcParams["figure.figsize"]=[16,9] 
 
plt.plot(result.index.year[result.month=='Apr'], result['DC'][result.month=='Apr'],  label='Avril', linewidth=2, c=color[0])      
plt.plot(result.index.year[result.month=='May'], result['DC'][result.month=='May'],  label='Mai', linewidth=2, c=color[1])
plt.plot(result.index.year[result.month=='Jun'], result['DC'][result.month=='Jun'],  label='Juin', linewidth=2, c=color[2])
plt.plot(result.index.year[result.month=='Jul'], result['DC'][result.month=='Jul'],  label='Juillet', linewidth=2, c=color[3])
plt.plot(result.index.year[result.month=='Aug'], result['DC'][result.month=='Aug'],  label='Août', linewidth=2, c=color[4])

plt.legend(loc="upper left", markerscale=1., scatterpoints=1, fontsize=20)

#ax.set_xlim(result.index.year[0], result.index.year[-1])
plt.xticks(range(result.index.year[0]-1, result.index.year[-1]+1, 10), fontsize=14)
plt.yticks( fontsize=14)

ax1.grid(axis = "x", linestyle = "--", color='black', linewidth=0.25, alpha=0.5)
ax1.grid(axis = "y", linestyle = "--", color='black', linewidth=0.25, alpha=0.5)
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
         
xposition = [1970, 2000, 2010, 2040, 2070]

for xc in xposition:
    plt.axvline(x=xc, color='k', linestyle='--')
for label in ax1.get_yticklabels():
    label.set_fontsize(20)
for tick in ax1.xaxis.get_major_ticks():
    tick.label.set_fontsize(20)  
    
plt.setp(plt.gca().get_xticklabels(), rotation=0, ha="right")

plt.xlabel('Année', fontsize=20, color='black', weight='semibold')
plt.ylabel('DC', fontsize=20, color='black', weight='semibold')
plt.title('Variabilités interannuelles des moyennes mensuelles d\'indices de sécheresse sur Pessamit \n', fontsize=20, color='black', weight='semibold')

my_pal = {"RCMs_histo": "grey", "RCMs_rcp45": "blue", "RCMs_rcp85":"red"}

plt.yticks( fontsize=14)
    
plt.savefig('K:/PROJETS/PROJET_CLIMHUNOR/Atlas/Atlas_figures/VI_MONTH_Dry_Code.png', bbox_inches='tight', format='png', dpi=1000)
plt.show()  
plt.close()


