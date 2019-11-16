#!/bin/bash

#this script uses ogrinfo to write the file's basename (no path, no ext) to an new attribute field called "filename". Then it adds each cutline into
#into a master cutline index shapefile called "master_cutline_index.shp"

for f in *.shp
do
  #get the basename
  basename=${f%.shp}
  echo $basename

  #create the field
  ogrinfo $f -sql "ALTER TABLE $basename ADD COLUMN filename character(15)"
  #add the basename to the field
  ogrinfo $f -dialect SQLite -sql "UPDATE $basename SET filename = '$basename'"
  #send the cutline with new field to the master_cutline_index
  ogr2ogr -update -append niihau_gto_raw_merge.shp $f
done
