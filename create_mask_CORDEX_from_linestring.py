# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:06:25 2019

@author: guillaume
"""
import xarray as xr
import matplotlib.pylab as plt
import warnings; warnings.filterwarnings(action='ignore')
import numpy as np
from osgeo import ogr
import geopandas as gpd

ds = xr.open_mfdataset('K:/PROJETS/PROJET_CLIMHUNOR/DRY/anomalie_ensemble_6_RCMs_Pilotes_GCMs_rcp85_CORDEX_NAM44_ll_DC_2011-2040_1971-2000.nc')

lon = ds['lon'].values
lat = ds['lat'].values

from shapely.geometry import Polygon, mapping

def linestring_to_polygon(fili_shps):
    gdf = gpd.read_file(fili_shps) #LINESTRING
    geom = [x for x in gdf.geometry]
    all_coords = mapping(geom[0])['coordinates']
    lats = [x[1] for x in all_coords]
    lons = [x[0] for x in all_coords]
    linestr = Polygon(zip(lons, lats))
    return gpd.GeoDataFrame(index=[0], crs=gdf.crs, geometry=[linestr])

poly_shapes = linestring_to_polygon("./NITASSINAN/nitassinan_l.shp")
poly_shapes.to_file('./NITASSINAN/nitassinan_l2.shp')
shapes = gpd.read_file("./NITASSINAN/nitassinan_l2.shp")

tmpWGS84 = shapes.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})
tmpWGS84.loc[0, 'geometry']
#tmpWGS84.to_file('Outaouais_WGS84.shp')
tmpWGS84.to_file('nitassinan_84.shp')
tmpWGS84.plot()
def get_mask(lons2d, lats2d, shp_path="", polygon_name=None):
    """
    Assumes that the shape file contains polygons in lat lon coordinates
    :param lons2d:
    :param lats2d:
    :param shp_path:
    :rtype : np.ndarray
    The mask is 1 for the points inside of the polygons
    """
    ds = ogr.Open(shp_path)
    """
    :type : ogr.DataSource
    """

    xx = lons2d.copy()
    yy = lats2d

    # set longitudes to be from -180 to 180
    xx[xx > 180] -= 360

    mask = np.zeros(lons2d.shape, dtype=int)
    nx, ny = mask.shape

    pt = ogr.Geometry(ogr.wkbPoint)

    for i in range(ds.GetLayerCount()):
        layer = ds.GetLayer(i)
        """
        :type : ogr.Layer
        """

        for j in range(layer.GetFeatureCount()):
            feat = layer.GetFeature(j)
            """
            :type : ogr.Feature
            """

            # Select polygons by the name property
            if polygon_name is not None:
                if not feat.GetFieldAsString("name") == polygon_name:
                    continue

            g = feat.GetGeometryRef()
            """
            :type : ogr.Geometry
            """

            assert isinstance(g, ogr.Geometry)

            for pi in range(nx):
                for pj in range(ny):
                    pt.SetPoint_2D(0, float(xx[pi, pj]), float(yy[pi, pj]))

                    mask[pi, pj] += int(g.Contains(pt))

    return mask


#mask=get_mask(lon2d,lat2d,shp_path="Outaouais_WGS84.shp")
#np.save('Outaouais.npy',mask)
mask=get_mask(lon,lat,shp_path="nitassinan_84.shp")

np.save('nitassinan_84.npy',mask)
print(u'Terminé')

data = ds['DC'][1].where(mask==1)/ds['DC'][1].where(mask==1)

data.plot()

data.to_netcdf('nitassinan_CORDEX.nc')
