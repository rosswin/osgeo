# osgeo

Random widgets for working with osgeo data. Bulit and tested on Ubuntu 18.04 and Python 3.

## fast_tindex.py

A script that generates a vector tile index from folders of georeferenced raster imagery. Typically used to see the boundaries of satellite imagery in GIS software. However, this script only reads header information and does it in parallel. So it is very fast. 

If you inputed the tiles of coastal imagery displayed below, you would get the red checkerboxes in this example:

![gpkg_output](/images/fast_tindex_example.png)

 ### USAGE:
 
 `fast_tindex.py -f my_file_list.txt -o my_tindex.gpkg -e epsg:26904`
 
### FLAGS:
* -f File List:  A comma-delimted txt/csv list of absolute file paths, one file per line. Best generated using the command:
`find </absolute/path/to/your/input/directory> -name <.your_ext> >> file_list.txt`
  * Example: -e gpkg
  * Example: -e shp
* -o Out File : Absolute path to where you would like your tile index geopackage stored. Must contain the file name in the path AND end in .gpkg. GPKGS ONLY!!!!
  * Example: ~/mydir/mygpkg.gpkg
  * Example: myshp.shp
* -e EPSG CODE: The EPSG code of your input image data. Only one CRS is supported, and the script does not check for this. Must be in the format 'epsg:<XXXXX>' where <XXXXX> is a 5 digit EPSG code (no <>, just numbers). See epsg.io for more info. 
  * Example: filename
  * Example: orig_fname
 * -l Log File: Include this flag to write a logfile alongside your geopackage.
 

## vector_merge.sh

A handy little shell script that takes OGR-compliant geospatial vector formats (mostly shapefiles and geopackages) and merges them. It uses ogr2ogr under the hood to ensure that we can cross straingt from shp to gpkg, and back again. The real contibution is the -a flag, which allows the user to specify a field to preserve each of the original file's name within the merged file's attribute table.
                
### USAGE:

When outputting a gpkg, the original files are added as layers inside the gpkg you choose. The following command line:

`vector_merge.sh -e gpkg -o Statewide_Points.gpkg -a island`

Produces the following output:

![gpkg_output](/images/vector_merge_gpkg_out.png)

Meanwhile, a shapefile export is pretty straightforward. The following command line:

`vector_merge.sh -e shp -o Statewide_Points.shp -a island`

Produces the following output:

![shp_output](/images/vector_merge_shp_out.png)

An outside merge is used to merge the attribute tables, so no information is lost. And, of course, the -a flag is respected in the merged file's resulting attribute table no matter what output format you use:

![attr_output](/images/vector_merge_attr_out.png)

### FLAGS:
* -e Extension: This is a plain text extension to search the current directory for. These will be merged into output (-o). 
  * Example: -e gpkg
  * Example: -e shp
* -o Out File : This is the merged output file. See notes above about behavior when outputting gpkgs vs shps.
  * Example: ~/mydir/mygpkg.gpkg
  * Example: myshp.shp
* -a Attribute: This is name of a field that will be stored in the merged output file's attribute table. This field stores the original file's name. Note, if shapefiles involved you must respect field name rules: must start w/ letter and 15 characters or less.
  * Example: filename
  * Example: orig_fname


