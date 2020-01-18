# osgeo

Random widgets for working with osgeo data. Bulit and tested on Ubuntu 18.04 and Python 3.

## fast_tindex.py



## vector_merge.sh

A handy little shell script that takes OGR-compliant geospatial vector formats (mostly shapefiles and geopackages) and merges them. It uses ogr2ogr under the hood to ensure that we can cross straingt from shp to gpkg, and back again. The real contibution is the -a flag, which allows the user to specify a field to preserve each of the original file's name within the merged file's attribute table.

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


