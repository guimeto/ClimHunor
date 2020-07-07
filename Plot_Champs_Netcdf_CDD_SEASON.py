#-*- coding: utf-8 -*-
#####################################################

# Importation des modules nécessaire au traitement des données

from netCDF4 import Dataset
import matplotlib.pylab as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib as mpl

#########################################################
Saison=['JJA']
Name=['Summer']
NameFr=['Ete']
period=['2071-2100']

scenario=['rcp85']
nb_model=['9']
import pandas as pd
BV_border1 = pd.read_csv('./nitassinan_l_WGS84_pnts.csv', sep=',',skiprows = range(0, 1))
BV_border1.columns=["lon", "lat"]
BV_border1["lon"]=BV_border1["lon"].apply(lambda x: x.replace("(", "")).apply(pd.to_numeric,1)
BV_border1["lat"]=BV_border1["lat"].apply(lambda x: x.replace(")", "")).apply(pd.to_numeric,1)
BV_border1.head()
BV_border1.lon
BV_border1.append(BV_border1, ignore_index=True)
BV_border1.head()
def plot_background(ax):
#    crs_lonlat=ccrs.PlateCarree()
    ax.set_extent([-90,-62,40,60])
    ax.coastlines(resolution='110m');
    ax.add_feature(cfeature.OCEAN.with_scale('50m'))      
    ax.add_feature(cfeature.LAND.with_scale('50m'))       
    ax.add_feature(cfeature.LAKES.with_scale('50m'))     
    ax.add_feature(cfeature.BORDERS.with_scale('50m'))    
    ax.add_feature(cfeature.RIVERS.with_scale('50m'))    
    coast = cfeature.NaturalEarthFeature(category='physical', scale='10m',    
                        facecolor='none', name='coastline')
    ax.add_feature(coast, edgecolor='black')
    
    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none')

    ax.add_feature(states_provinces, edgecolor='gray')
  #  ax.gridlines(crs=crs_lonlat,
  #               xlocs = np.arange(-180,180,15),
  #               ylocs = np.arange(-180,180,15),
  #               draw_labels = True)   
   
    return ax

Y=np.array([[51,51,0],[51,102,0],[102,102,51],[102,153,51],[153,204,102],[153,255,158],[204,255,153],[204,255,204],\
            [153,0,255],[153,51,255],[153,102,255],[102,51,204],[51,0,153],[0,51,153],[51,102,204],[102,153,255],\
            [31,255,255],[102,255,255],[153,255,255],[204,255,255],\
            [255,255,204],[255,255,102],[255,255,0],[255,204,102],[255,204,51],[255,204,0],\
            [255,153,51],[255,102,0],[255,51,0],[255,51,51],[255,0,0],[204,51,51],\
            [204,0,0],[153,51,51],[153,0,0],[102,51,51],[102,0,0],[102,51,0],[51,0,0],[0,0,0]])/255.
colbar=mpl.colors.ListedColormap(Y)

#########################################################
#Boucle pour sortir tous les graphiques et les sauvegardés
# Lecture du fichier et affichage des métadonnées
for s in range(0,1,1):
  for t in range(0,1,1):
    for i in range(0,4,1): 
########################  OUVERTURE DU CHAMPS A LIRE  ########
        rep1='K:/PROJETS/PROJET_CORDEX/CORDEX-NAM44/ANOMALIE_ENSEMBLE/SAISON/CDD/'
        rep2='anomalie_ensemble_'+nb_model[s]+'_RCMs_Pilotes_GCMs_'+scenario[s]+'_CORDEX_NAM44_ll_CDD_'+period[t]+'_1971-2000_'+Saison[i]+'.nc'
        filename=rep1+rep2
        nc_fid=Dataset(filename,'r')  
        lats = nc_fid.variables['lat'][:]  # Extrait et copie les données du fichier NetCDF
        lons = nc_fid.variables['lon'][:]
        time = nc_fid.variables['time'][:]
        Vals = nc_fid.variables['CDD'][:].squeeze() 

########################  OUVERTURE DU CHA MPS SIGNIFICATIF  ########
        rep3='K:/PROJETS/PROJET_CORDEX/CORDEX-NAM44/ANOMALIE_ENSEMBLE/SAISON/SIGNIFICATIF_sigma/CDD/'
        rep4='anomalie_ensemble_60percent_significatif_'+nb_model[s]+'_RCMs_Pilotes_GCMs_'+scenario[s]+'_CORDEX_NAM44_ll_CDD_'+period[t]+'_1971-2000_'+Saison[i]+'.nc'
        filename=rep3+rep4
        nc_fid=Dataset(filename,'r')  
        lats = nc_fid.variables['lat'][:]  # Extrait et copie les données du fichier NetCDF
        lons = nc_fid.variables['lon'][:]
        time = nc_fid.variables['time'][:]
        Vals2 = nc_fid.variables['CDD'][:].squeeze() 

##########################################################
        fig = plt.figure(figsize=(28,16))         
        crs=ccrs.LambertConformal()
    #    crs=ccrs.PlateCarree()
        ax = plt.axes(projection=crs)
        plot_background(ax)
        
        ax.plot(-69.72, 48.15, "bo", markersize=7, transform=ccrs.Geodetic())
        ax.text(-69.5, 48.17, "Tadoussac", color='blue', fontsize=20, fontweight='bold', transform=ccrs.Geodetic())
        
        ax.plot(-66.4, 50.21, "bo", markersize=7,  color='blue',  transform=ccrs.Geodetic())
        ax.text(-66.2, 50.22, "Sept-îles", color='blue', fontsize=20, fontweight='bold', transform=ccrs.Geodetic())
        
        mycmap=colbar
       # mycmap = mpl.cm.get_cmap('afmhot_r', 50)
        #mycmap.set_under("w")
       # mycmap.set_over("darkred") 
    
        
        mm = ax.contourf(lons,\
                   lats,\
                   Vals,\
                   transform=ccrs.PlateCarree(),\
                   levels=np.arange(-4, 4.1, 0.5), \
                   cmap=mycmap )
        
    
        #ax.stock_img();      
        ax.gridlines()

        fig.canvas.draw()                 
        cs = ax.plot(BV_border1.lon,BV_border1.lat, transform=ccrs.PlateCarree(), color='blue', linewidth=4, label='Nitassinan Pessamit')
        
        plt.legend(loc="upper left", markerscale=2., fontsize=20)
        # Define gridline locations and draw the lines using cartopy's built-in gridliner:
        xticks = np.arange(-150.0,-40.0,20)
        yticks =np.arange(10,80,10)
        
        fig.canvas.draw()
                      
        cs = ax.scatter(lons[Vals2==1],lats[Vals2==1], transform=ccrs.PlateCarree(), marker='.', s=2, color='k')
        
        cbar = plt.colorbar(mm,  shrink=0.75, drawedges='True', ticks=np.arange(-4.0, 4.1, 0.5), extend='both')
        cbar.ax.tick_params(labelsize=17) 
        plt.xlabel(u'\n\n\nAbsolute anomaly of maximum consecutif dry days CDD',size='x-large')        
        string_title=u'Season anomaly of maximum consecutif dry days CDD \n in '+Name[i]+'\n  ENSEMBLE of '+nb_model[s]+' RCMs with scenario '+scenario[s]+' ('+period[t]+') vs (1971-2000))\n\n'        
        plt.title(string_title, size='xx-large')       
        plt.savefig('K:/PROJETS/PROJET_CLIMHUNOR/Atlas/Atlas_figures/figures_22_23/anomalie_ensemble_'+nb_model[s]+'_RCMs_Pilotes_GCMs_'+scenario[s]+'_CORDEX_NAM44_ll_CDD_'+period[t]+'_1971-2000_'+Saison[i]+'.png', bbox_inches='tight', pad_inches=0.1)
        plt.show()  
        plt.close()
        

print('Terminé')




