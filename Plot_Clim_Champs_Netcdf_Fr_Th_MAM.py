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
period=['2071_2100']
list_month = ["01"]

##scenario=['rcp45','rcp85']
##nb_model=['6','9']
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
    ax.set_extent([-80,-62,45,60])
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
   
#Y=np.array([[146, 0, 0],[193, 0, 0],[224, 2, 4],[247, 3, 5],[194, 90, 14],[235, 104, 45],[252, 191, 1],[251, 217, 106],\
#            [254, 253, 8],[239, 241, 160],[199, 222, 176],[142, 211, 82],[2, 176, 85],[85, 128, 50],[190, 213, 238],\
#            [140, 169, 218],[19, 167, 242],[42, 116, 180],[33, 75, 124],\
#            [117, 47, 160],[73, 37, 104]])/255.    
    
    
#colbar=mpl.colors.ListedColormap(Y[::-1])
colbar=mpl.colors.ListedColormap(Y[20:])




#########################################################
#Boucle pour sortir tous les graphiques et les sauvegardés
# Lecture du fichier et affichage des métadonnées
for s in range(0,1,1):
  for t in range(0,1,1):
    for i in list_month:
########################  OUVERTURE DU CHAMPS A LIRE  ########
        rep1='K:/PROJETS/PROJET_CORDEX/CORDEX-NAM44/MOYENNE_ENSEMBLE/SAISON/Fr_Th/'
        #rep2='MOYENNE_ENSEMBLE_9_RCMs_Pilotes_GCMs_histo_Fr_Th_1971_2000_DJF.nc'
        #rep2='MOYENNE_ENSEMBLE_9_RCMs_Pilotes_GCMs_rcp85_Fr_Th_2011_2040_DJF.nc'
        #rep2='MOYENNE_ENSEMBLE_9_RCMs_Pilotes_GCMs_rcp85_Fr_Th_2041_2070_DJF.nc'
        rep2='MOYENNE_ENSEMBLE_9_RCMs_Pilotes_GCMs_rcp85_Fr_Th_2071_2100_DJF.nc'
        
        filename=rep1+rep2
        nc_fid=Dataset(filename,'r')  
        lats = nc_fid.variables['lat'][:]  # Extrait et copie les données du fichier NetCDF
        lons = nc_fid.variables['lon'][:]
        time = nc_fid.variables['time'][:]
        Vals = nc_fid.variables['Fr_Th'][:].squeeze() 
                
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
       # mycmap = mpl.cm.get_cmap('jet', 40)
        
        mm = ax.contourf(lons,\
                   lats,\
                   Vals,\
                   transform=ccrs.PlateCarree(),\
                   levels=np.arange(0, 52.0, 2),\
                   cmap=colbar )
        
    
        ax.gridlines()
        fig.canvas.draw()
        cs = ax.plot(BV_border1.lon,BV_border1.lat, transform=ccrs.PlateCarree(), color='r', linewidth=4, label='Nitassinan Pessamit')
        plt.legend(loc="best", markerscale=2., fontsize=20)
        
        # Define gridline locations and draw the lines using cartopy's built-in gridliner:
        xticks = np.arange(-150.0,-40.0,20)
        yticks =np.arange(10,80,10)
        
        fig.canvas.draw()
      
        cbar = plt.colorbar(mm,  shrink=0.75, drawedges='True', ticks=np.arange(0, 52.0, 2.0), extend='both',label='Jours')
        cbar.ax.tick_params(labelsize=17) 
        ax = cbar.ax
        text = ax.yaxis.label
        font = mpl.font_manager.FontProperties(size=25)
        text.set_font_properties(font)
              
        string_title=u'Climatologie du nombre de jours de gel/degel en hiver '+period[t]+'\n'        
        plt.title(string_title, size='xx-large')       
        plt.savefig('K:/PROJETS/PROJET_CLIMHUNOR/Atlas/Atlas_figures/figures_24_25/climatology_ensemble_'+nb_model[s]+'_RCMs_Pilotes_GCMs_'+scenario[s]+'_CORDEX_NAM44_ll_Fr_Th_'+period[t]+'_DJF.png', bbox_inches='tight', pad_inches=0.1)
        plt.show()  
        plt.close()
        

print('Terminé')






