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

rep1='K:/PROJETS/PROJET_CORDEX/CORDEX-NAM44/ANOMALIE_ANNEE_INTER_ANNUELLE/'
variable_in = 'Mean_tasmax'

list_period = ['2011-2040','2041-2070','2071-2100']

path_rcp45 =  ['CANRCM4_CanESM2_rcp45',           
               'CRCM5-v1_CCCma-CanESM2_rcp45', 'CRCM5-v1_MPI-M-MPI-ESM-LR_rcp45' ,  
               'HIRHAM5_ICHEC-EC-EARTH_rcp45',  
               'RCA4.v1_CCCma-CanESM2_rcp45','RCA4.v1_ICHEC-EC-EARTH_rcp45']

path_rcp85 = ['CANRCM4_CanESM2_rcp85',            
              'CRCM5-v1_CCCma-CanESM2_rcp85','CRCM5-v1_MPI-M-MPI-ESM-MR_rcp85',    
              'HIRHAM5_ICHEC-EC-EARTH_rcp85',  
              'RCA4.v1_CCCma-CanESM2_rcp85','RCA4.v1_ICHEC-EC-EARTH_rcp85']

path_histo = ['CANRCM4_CanESM2_historical',           
              'CRCM5-v1_CCCma-CanESM2_historical', 'CRCM5-v1_MPI-M-MPI-ESM-LR_historical',   
              'HIRHAM5_ICHEC-EC-EARTH_histo',  
              'RCA4.v1_CCCma-CanESM2_histo','RCA4.v1_ICHEC-EC-EARTH_histo']

list_rcp45 = ['CANRCM4_NAM-44_ll_CanESM2_rcp45',             
              'CRCM5-v1_NAM-44_ll_CCCma-CanESM2_rcp45', 'CRCM5-v1_NAM-44_ll_MPI-M-MPI-ESM-LR_rcp45' ,
              'HIRHAM5_NAM-44_ll_ICHEC-EC-EARTH_rcp45', 
              'RCA4.v1_NAM-44_ll_CCCma-CanESM2_rcp45','RCA4.v1_NAM-44_ll_ICHEC-EC-EARTH_rcp45']

list_rcp85 = ['CANRCM4_NAM-44_ll_CanESM2_rcp85',            
              'CRCM5-v1_NAM-44_ll_CCCma-CanESM2_rcp85','CRCM5-v1_NAM-44_ll_MPI-M-MPI-ESM-MR_rcp85', 
              'HIRHAM5_NAM-44_ll_ICHEC-EC-EARTH_rcp85',  
              'RCA4.v1_NAM-44_ll_CCCma-CanESM2_rcp85','RCA4.v1_NAM-44_ll_ICHEC-EC-EARTH_rcp85']

list_histo = ['CANRCM4_NAM-44_ll_CanESM2_historical',           
              'CRCM5-v1_NAM-44_ll_CCCma-CanESM2_historical', 'CRCM5-v1_NAM-44_ll_MPI-M-MPI-ESM-LR_historical',   
              'HIRHAM5_NAM-44_ll_ICHEC-EC-EARTH_histo',  
              'RCA4.v1_NAM-44_ll_CCCma-CanESM2_histo','RCA4.v1_NAM-44_ll_ICHEC-EC-EARTH_histo']
df_rcp45 = []
matrix_45 = []
for period in list_period: 
    globals()['flattened_list_'+period] = []
    for i in range(0,len(list_rcp45)):
        filename= rep1 + path_rcp45[i] + '/' + period + '/' + variable_in + '/anomalie_' +  list_rcp45[i] +  '_' + variable_in + '_' + period  + '_1971-2000.nc'   
        nc = netCDF4.Dataset(filename)
        var = nc.variables[variable_in][:]  
        lats = nc.variables['lat'][:]; lons = nc.variables['lon'][:]
        #lon2d, lat2d = np.meshgrid(lon, lat)
        #lats = lat2d[:]; lons = lon2d[:]
        if list_rcp45[i] == 'CANRCM4_NAM-44_ll_CanESM2_rcp45':
            latbounds = [ 47 , 51 ]
            lonbounds = [ 288 , 296 ]
        else:
            latbounds = [ 47 , 51 ]
            lonbounds = [ -72 , -64 ]
            
        subset = ((lats > latbounds[0]) & (lats < latbounds[1]) & 
             (lons > lonbounds[0]) & (lons < lonbounds[1]))
        #mask = np.where(subset)
        data=pd.DataFrame(var[:,subset], dtype='float') 
        globals()['flattened_list_'+period].append(data.mean(axis=1))        
    df_rcp45.append(pd.DataFrame(globals()['flattened_list_'+period]).T) 

TIME=[]
for y in range(int(list_period[0].split('-')[0]),int(list_period[-1].split('-')[-1])+1,1):
    TIME.append(datetime.strptime(str(y), '%Y'))
    
df_rcp45 = pd.concat(df_rcp45)
df_rcp45 = df_rcp45.std(axis=1).to_frame()    
         
df_rcp45['Date'] = TIME   
df_rcp45.index = df_rcp45['Date']
df_rcp45 = df_rcp45.drop(["Date"], axis=1)  


df_rcp85 = []
matrix_85 = []
for period in list_period: 
    globals()['flattened_list_'+period] = []
    for i in range(0,len(list_rcp85)):
        filename= rep1 + path_rcp85[i] + '/' + period + '/' + variable_in + '/anomalie_' +  list_rcp85[i] +  '_' + variable_in + '_' + period  + '_1971-2000.nc'   
        nc = netCDF4.Dataset(filename)
        var = nc.variables[variable_in][:]  
        lats = nc.variables['lat'][:]; lons = nc.variables['lon'][:]
        #lon2d, lat2d = np.meshgrid(lon, lat)
        #lats = lat2d[:]; lons = lon2d[:]
        if list_rcp85[i] == 'CANRCM4_NAM-44_ll_CanESM2_rcp85':
            latbounds = [ 47 , 51 ]
            lonbounds = [ 288 , 296 ]
        else:
            latbounds = [ 47 , 51 ]
            lonbounds = [ -72 , -64 ]
            
        subset = ((lats > latbounds[0]) & (lats < latbounds[1]) & 
             (lons > lonbounds[0]) & (lons < lonbounds[1]))
        #mask = np.where(subset)
        data=pd.DataFrame(var[:,subset], dtype='float') 
        globals()['flattened_list_'+period].append(data.mean(axis=1))        
    df_rcp85.append(pd.DataFrame(globals()['flattened_list_'+period]).T) 
    
df_rcp85 = pd.concat(df_rcp85)
df_rcp85 = df_rcp85.std(axis=1).to_frame()   

df_rcp85['Date'] = TIME   
df_rcp85.index = df_rcp85['Date']
df_rcp85 = df_rcp85.drop(["Date"], axis=1)  

df_histo = []
 
globals()['flattened_list_'+period] = []
for i in range(0,len(list_histo)):
    filename= rep1 + path_histo[i] + '/1971-2000/' + variable_in + '/anomalie_' +  list_histo[i] +  '_' + variable_in + '_1971-2000_1971-2000.nc'   
    nc = netCDF4.Dataset(filename)
    var = nc.variables[variable_in][:]  
    lats = nc.variables['lat'][:]; lons = nc.variables['lon'][:]
    if list_histo[i] == 'CANRCM4_NAM-44_ll_CanESM2_historical':
        latbounds = [ 47 , 51 ]
        lonbounds = [ 288 , 296 ]
    else:
        latbounds = [ 47 , 51 ]
        lonbounds = [ -72 , -64 ]
        
    subset = ((lats > latbounds[0]) & (lats < latbounds[1]) & 
         (lons > lonbounds[0]) & (lons < lonbounds[1]))
    #mask = np.where(subset)
    data=pd.DataFrame(var[:,subset], dtype='float') 
    globals()['flattened_list_'+period].append(data.mean(axis=1))        
df_histo.append(pd.DataFrame(globals()['flattened_list_'+period]).T) 

TIME=[]
for y in range(1971,2001,1):
    TIME.append(datetime.strptime(str(y), '%Y'))
    
    
df_histo = pd.concat(df_histo)
df_histo = df_histo.std(axis=1).to_frame()     

df_histo['Date'] = TIME   
df_histo.index = df_histo['Date']
df_histo = df_histo.drop(["Date"], axis=1)  

result = []
result = pd.DataFrame({'rcp45': df_rcp45.iloc[:,0],'rcp85': df_rcp85.iloc[:,0], 'histo': df_histo.iloc[:,0]},
        columns = ['rcp45','rcp85','histo']) 

color = ['black','blue', 'red']
fig = plt.figure(figsize=(22, 12)) 
gs = gridspec.GridSpec(1, 2, width_ratios=[6, 1]) 
gs.update( wspace=0.04)
ax1 = plt.subplot(gs[0])

plt.rcParams["figure.figsize"]=[16,9]       #  
plt.plot(result.index.year, result['histo'][:],  label='Historique', linewidth=2, c=color[0])
plt.plot(result.index.year, result['rcp45'][:],  label='RCP4.5', linewidth=2, c=color[1])
plt.plot(result.index.year, result['rcp85'][:],  label='RCP8.5', linewidth=2, c=color[2])

plt.legend(loc="upper left", markerscale=1., scatterpoints=1, fontsize=20)

#ax.set_xlim(result.index.year[0], result.index.year[-1])
plt.xticks(range(result.index.year[0]-1, result.index.year[-1]+1, 10), fontsize=14)
plt.yticks( fontsize=14)
# Don't allow the axis to be on top of your data
ax1.set_axisbelow(True)

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
    
plt.ylabel('°C', fontsize=20, color='black', weight='semibold')

    
ax2 = ax1.twinx()
ax2.set_ylim(ax1.get_ylim())    
for tick in ax2.xaxis.get_major_ticks():
    tick.label.set_fontsize(20)
for label in ax2.get_yticklabels():
    label.set_fontsize(20)
    
ax2.set_ylabel('°C', fontsize=20, color='black', weight='semibold')
    
    
plt.setp(plt.gca().get_xticklabels(), rotation=0, ha="right")
plt.xlabel('Année', fontsize=20, color='black', weight='semibold')
plt.title('Variabilités interannuelles de l\'écart type inter modèle de la température maximale journalière \n', fontsize=20, color='black', weight='semibold')


plt.savefig('K:/PROJETS/PROJET_CLIMHUNOR/Atlas/Atlas_figures/figure3/VI_YEAR_Sigma_Mean_tasmax.png', bbox_inches='tight', format='png', dpi=1000)    
plt.show()  
plt.close()


