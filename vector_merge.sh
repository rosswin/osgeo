#!/bin/bash

# WRITTEN BY W. ROSS WINANS
# OCT 2019

#NOTE July 2020: if using GDAL 2.2+ then checkout ogrmerge.py. It has all of this functionality and more. This script could become useful again if it used multiprocessing. 

#TODO:
#1. ogr2ogr spits out a ton of warnings and errors. Is there a way to mute these... or even maybe fix them?
#2. Add verbosity flag.
#3. Add a feature to only create one layer in an output gpkg.
#4. Add tons of error checking. Currently there is none.
#5. Explore and document other geospatial formats stability and performance.

e_flag=''
o_flag=''
a_flag=''

print_usage(){
  printf "
  VECTOR_MERGE USAGE:
  
  This script quickly merges OGR-supported vector formats. It has only been tested to merge shp or gpkg, but should theoretically work
  on other OGR formats. 
  
  NOTES:
  If you request a shp output, all input files will be placed into a single output shapefile with a user-specified
  field to store the orginal file's name in the attribute table (-a). 
  
  If you request a gpkg output, all the input files will be a layer in the gpkg with their original file name,
  note that each of these gpkg layers will still contain the user-specified field to store the original filename (-a).
  
  FLAGS:
  -e Extension: This is a plain text extension to search the current directory for. These will be merged into output (-o). 
                Example: -e gpkg
                Example: -e shp
  -o Out File : This is the merged output file. See notes above about behavior when outputting gpkgs vs shps.
                Example: ~/mydir/mygpkg.gpkg
                Example: myshp.shp
  -a Attribute: This is name of a field that will be stored in the merged output file's attribute table. This field stores the original
                file's name. Note, if shapefiles involved you must respect field name rules: must start w/ letter and 15 characters or less.
                Example: filename
                Example: orig_fname

  "
}

while getopts 'e:o:a:v' flag; do
  case "${flag}" in
  e) e_flag="${OPTARG}" ;;
  o) o_flag="${OPTARG}" ;;
  a) a_flag="${OPTARG}" ;;
  *) print_usage 
      exit 1 ;;
  esac
done

echo "Intitalized with:"
echo "Extension: "${e_flag}""
echo "Out File : "${o_flag}""
echo "Key Field: "${a_flag}""

for f in *."${e_flag}"
do

#get the basename of our merged files so we can document in the attr table.
basename=${f%."${e_flag}"}

echo "Found:               "${f}""
echo "Extracted basename: "${basename}""
echo "\n"

#create an attribute field our current file's attr table to store the orginal file's name, 
#then we will preserve that when we merge all files in the final step
ogrinfo "${f}" -sql "ALTER TABLE "${basename}" ADD COLUMN "${a_flag}" character(15)"

#add the basename to the field we created on the original file
ogrinfo "${f}" -dialect SQLite -sql "UPDATE "${basename}" SET "${a_flag}" = '$basename'"

#send the original file, with its name in its attribute table, to our final, merged file.
#note: ogr2ogr is like a swiss army knife. it just knows what to do based on attr table.
ogr2ogr -update -append "${o_flag}" "${f}"

done
