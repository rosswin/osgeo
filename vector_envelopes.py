#!/usr/bin/env python
# coding: utf-8
#!/usr/bin/env python
# coding: utf-8

import os
import glob

from concurrent.futures import ProcessPoolExecutor

from optparse import OptionParser

import rasterio
from rasterio.plot import show
from rasterio.mask import mask

import fiona
from shapely import geometry

import numpy as np

def write_envelope_from_image(in_path):
    with rasterio.open(in_path, 'r') as dataset:
        print(f"opened: {in_path}")

        #(lon, lat) of top left corner
        tl = geometry.Point(dataset.bounds.left, dataset.bounds.top)
        #(lon, lat) of bottom left corner
        bl = geometry.Point(dataset.bounds.left, dataset.bounds.bottom)
        #(lon, lat) of top right corner
        tr = geometry.Point(dataset.bounds.right, dataset.bounds.top)
        #(lon, lat) of bottom right corner
        br = geometry.Point(dataset.bounds.right, dataset.bounds.bottom)

        point_list = [tl, tr, br, bl]
        envelope = geometry.Polygon([[p.x, p.y] for p in point_list])

        schema = {'geometry': 'Polygon',
                  'properties': {}
                 }

        out_path = os.path.splitext(in_path)[0] + '.shp'
        print(f"{out_path}")

        with fiona.open(out_path, 'w', 'ESRI Shapefile', schema) as c:
            ## If there are multiple geometries, put the "for" loop here
            c.write({
                'geometry': geometry.mapping(envelope),
                'properties': {},
            })
            print(f"wrote: {out_path}")

def merge_shapefiles(in_path):


if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-e", "--extension", help="Search directory for files with this extension. Must be a rasterio-compliant image format. Must be quoted.", dest='in_ext')

    (opts, args) = parser.parse_args()

    #prepare a list of input files
    current_directory = os.getcwd()
    in_paths = glob.glob(os.path.join(current_directory, opts.in_ext))

    with ProcessPoolExecutor() as executor:
        executor.map(write_envelope_from_image, in_paths)
