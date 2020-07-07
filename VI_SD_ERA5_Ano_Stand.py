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

filename= 'J:/REANALYSES/ERA5/SWE_Cumul_Nittasinan/ERA5_SWE_Stand_anomalie_1981_2019_vs_1981_2010_M3-31.nc' 
sd_dataset = xr.open_mfdataset(filename)
df2 = sd_dataset.sd.mean(dim=('lon','lat')).to_dataframe("sd").dropna(how='all')  

fig = plt.figure(figsize=(22, 12)) 
gs = gridspec.GridSpec(1, 2, width_ratios=[6, 1]) 
gs.update( wspace=0.04)
ax1 = plt.subplot(gs[0])
plt.rcParams["figure.figsize"]=[16,9]       #  
plt.plot(df2.index.year, df2['sd'][:],  label='ERA5-Land', linewidth=2, c='blue')

plt.legend(loc="upper left", markerscale=1., scatterpoints=1, fontsize=20)

#ax.set_xlim(result.index.year[0], result.index.year[-1])
plt.xticks(range(df2.index.year[0]-1, df2.index.year[-1]+1, 10), fontsize=14)
plt.yticks( fontsize=14)
# Don't allow the axis to be on top of your data
ax1.set_axisbelow(True)

ax1.grid(axis = "x", linestyle = "--", color='black', linewidth=0.25, alpha=0.5)
ax1.grid(axis = "y", linestyle = "--", color='black', linewidth=0.25, alpha=0.5)
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
         
#xposition = [1970, 2000, 2010, 2040, 2070]
#for xc in xposition:
#    plt.axvline(x=xc, color='k', linestyle='--')
#for label in ax1.get_yticklabels():
#    label.set_fontsize(20)
#for tick in ax1.xaxis.get_major_ticks():
#    tick.label.set_fontsize(20)  
    
plt.setp(plt.gca().get_xticklabels(), rotation=0, ha="right")

plt.xlabel('Année', fontsize=20, color='black', weight='semibold')
plt.ylabel('', fontsize=20, color='black', weight='semibold')
plt.title('Variabilités interannuelles des anomalies standardisées de l\'épaisseur de neige au 31 mars par rapport à la normale 1981-2010 \n', fontsize=20, color='black', weight='semibold')
for label in ax1.get_yticklabels():
    label.set_fontsize(20)

plt.savefig('K:/PROJETS/PROJET_CLIMHUNOR/Atlas/Atlas_figures//VI_Ano_Stand_SD_31mars_vs_1981-2010.png', bbox_inches='tight', format='png', dpi=1000)
plt.show()  
plt.close()






