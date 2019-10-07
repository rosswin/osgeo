#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import multiprocessing
import logging

import rasterio

import fiona
from shapely import geometry

import geopandas as gpd
import pandas as pd

def return_extent(in_img):
    basename = os.path.splitext(os.path.basename(in_img))[0]

    with rasterio.open(in_img, 'r') as src:

        #(lon, lat) of top left corner
        tl = geometry.Point(src.bounds.left, src.bounds.top)
        #(lon, lat) of bottom left corner
        bl = geometry.Point(src.bounds.left, src.bounds.bottom)
        #(lon, lat) of top right corner
        tr = geometry.Point(src.bounds.right, src.bounds.top)
        #(lon, lat) of bottom right corner
        br = geometry.Point(src.bounds.right, src.bounds.bottom)

        point_list = [tl, tr, br, bl]
        envelope = geometry.Polygon([[p.x, p.y] for p in point_list])
        gs = gpd.GeoSeries(envelope)

        temp_dict = {'filename':[basename]}
        temp_df = pd.DataFrame(data=temp_dict)
        temp_gdf = gpd.GeoDataFrame(temp_df, crs=out_crs, geometry=gs)

        logging.info(f"{basename}, COMPLETE")
    return temp_gdf


# START EDITING #####################################
file_list = r"/media/ross/ssd/00_2015_DAR_marinedebris/maui/04_window_retile/jpg_list.txt"
out_dir = r"/media/ross/ssd/00_2015_DAR_marinedebris/maui/tiles_shp/"

out_path_gpkg = os.path.join(out_dir, 'maui_positive_tile_index.gpkg')

out_crs = {'init':'epsg:26904'}

#### STOP EDITING ###################################
#### MAIN ###########################################

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler(log_name),
        logging.StreamHandler()
    ])

with open(file_list, 'r') as f:
    in_paths = [line.strip() for line in f]

pool=multiprocessing.Pool()

results=pool.map(return_extent, in_paths[:10])

pool.close()
pool.join()

results_pd = pd.concat(results, ignore_index=True)

results_gpd = gpd.GeoDataFrame(results_pd, crs=out_crs, geometry='geometry')

results_gpd.to_file(out_path_gpkg, driver="GPKG")
logging.info(f"{out_path_gpkg}, WROTE")
