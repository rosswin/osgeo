#!/usr/bin/env python
# coding: utf-8

'''
Written by W. Ross Winans
Dec 2019

This script generates a tile index for a list of georeferenced imagery. Why do you need a separate script
for this? Because sometimes doing it from the command line and utilizing all available CPU cores is nice 
and I am too lazy to learn rio!

Here are the steps:
1. Take list of georeferenced imagery
2. Read each image headers in parallel, extract the bounds.
3. Compile these image tile bounds into a shapely object (polygon) that represents the full image extent.
4. Combine all of these polygons into a single tile index.
5. Write that file index to a geopackage.

NOTE
Had a ton of trouble with passing correct CRS to final merged gpkg. Don't touch it unless you want to own it!!

TODO
1. Autodetection of CRS. Ability to resolve conflicting/missing CRS- or at least throw up an error.
2. Add num_cores... I haven't added it because its so quick and low memory that it doesn't seem to matter.
3. Make it so the log output can easily be parsed for coordinates.
'''

import os
import time
import multiprocessing
import logging
import optparse

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
        temp_gdf = gpd.GeoDataFrame(temp_df, crs=src.crs, geometry=gs)

        #logging.info(f"{basename}: TL: {tl} | BL: {bl} | TR: {tr} | BR: {br}")
    return temp_gdf

if __name__ == "__main__":
    #handle our input arguments
    parser = optparse.OptionParser()

    parser.add_option('-f', '--filelist',
        action="store", dest="usr_file_list",
        type='string', help="A txt list of absolute file paths, one file per line.")

    parser.add_option('-o', '--outfile',
        action='store', dest='usr_out_file',
        type='string', help='Absolute file path to where you would like your tile index geopackage stored. Must contain the file name and end in .gpkg.')

    parser.add_option('-e', '--epsg',
        action='store', dest='usr_crs',
        type='string', help='The EPSG code of your input image data. Only one CRS is allowed. Must be in the format \'epsg:<XXXXX>\' where <XXXXX> is your 5-digit EPSG code. See epsg.io for more info.')
    
    parser.add_option('-l', '--logfile',
        action='store_true', dest='usr_log_bool',
        default=False, help='Including this flag will write a logfile with all the stdout and stderr alongside your geopackage.')
       
    options, args = parser.parse_args()

    #get the output path, make sure it exists. Also check that the extension is correct.
    out_dir, out_gpkg = os.path.split(options.usr_out_file)

    if not os.path.exists(out_dir) or out_gpkg.endswith('.gpkg') == False:
        logging.ERROR(f'Either {out_dir} does not exist. Or {out_gpkg} does not end in \'.gpkg\'. Aborting.')
        sys.exit(0)
    else:
        #check if the user wants a log file.
        if options.usr_log_bool == True:
            log_path = os.path.join(out_dir, 'log_' + time.strftime('%Y%m%d') + '.txt')
            print(f"Logging enabled. Writing to {log_path}")

            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s %(message)s",
                handlers=[
                    logging.FileHandler(log_path),
                    logging.StreamHandler()
                ])

        elif options.usr_log_bool == False:
            print(f"Logging NOT enabled.")
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s %(message)s",
                handlers=[
                    logging.StreamHandler()
                ])

        #parse the input filelist...
        with open(options.usr_file_list, 'r') as f:
            in_paths = [line.strip() for line in f]

        #chunk it up into a multiprocessing pool. 
        pool=multiprocessing.Pool()
        results=pool.map(return_extent, in_paths)
        pool.close()
        pool.join()

        #collect the pool results, concatenate all of them, specify our output crs, and merge into a tile index geodataframe
        results_pd = pd.concat(results, ignore_index=True)

        #format CRS the way that our program likes it.
        out_crs = {}
        out_crs['init'] = options.usr_crs

        logging.info(f"User specified CRS of {out_crs}")

        results_gpd = gpd.GeoDataFrame(results_pd, crs=out_crs, geometry='geometry')

        results_gpd.to_file(options.usr_out_file, driver="GPKG")
        logging.info("Successfully completed.")
