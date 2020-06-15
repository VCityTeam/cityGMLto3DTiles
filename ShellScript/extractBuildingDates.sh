# !/bin/sh

# This script detect the changes between CityGML files representing the
# buildings of the city of Lyon at two different vintages. The outputs are
# two graphML-JSON per borrough (one for 2009-2012 and one for 2012-2015:
# buildings
# It waits for the following parameters:
# $1: First date
# $2: First input-folder: a folder containing CityGML files representing
# buildings of the city of Lyon for a same vintage (corresponding to the
# provided "first date").
# $3: Second date
# $4: Second input-folder: a folder containing CityGML files representing
# buildings of the city of Lyon for a same vintage (corresponding to the
# provided "second date").
# $5 : output-folder: the folder containing the output graphML-JSON file.
# $6 : Path to 3DUSE Build folder

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

# Check that parameters are correctly provided
if [ $# != 6 ]
  then
	  echo "Six parameters must be provided to this script: first year, fist input folder (a folder containing the CityGML data at the first year), second year, second input folder (a folder containing the CityGML data at the second year), the output folder and the path to the 3DUSE Build folder."
    exit 1
fi

mkdir $5

# Buildings
${6}/src/utils/cmdline/extractBuildingDates --first_date ${1} --first_file ${2}/LYON_1ER_BATI_${1}.gml --second_date ${3} --second_file ${4}/LYON_1ER_BATI_${3}.gml --output_dir ${5}/LYON_1ER_${1}-${3}
${6}/src/utils/cmdline/extractBuildingDates --first_date ${1} --first_file ${2}/LYON_2EME_BATI_${1}.gml --second_date ${3} --second_file ${4}/LYON_2EME_BATI_${3}.gml --output_dir ${5}/LYON_2EME_${1}-${3}
${6}/src/utils/cmdline/extractBuildingDates --first_date ${1} --first_file ${2}/LYON_3EME_BATI_${1}.gml --second_date ${3} --second_file ${4}/LYON_3EME_BATI_${3}.gml --output_dir ${5}/LYON_3EME_${1}-${3}
${6}/src/utils/cmdline/extractBuildingDates --first_date ${1} --first_file ${2}/LYON_4EME_BATI_${1}.gml --second_date ${3} --second_file ${4}/LYON_4EME_BATI_${3}.gml --output_dir ${5}/LYON_4EME_${1}-${3}
${6}/src/utils/cmdline/extractBuildingDates --first_date ${1} --first_file ${2}/LYON_5EME_BATI_${1}.gml --second_date ${3} --second_file ${4}/LYON_5EME_BATI_${3}.gml --output_dir ${5}/LYON_5EME_${1}-${3}
${6}/src/utils/cmdline/extractBuildingDates --first_date ${1} --first_file ${2}/LYON_6EME_BATI_${1}.gml --second_date ${3} --second_file ${4}/LYON_6EME_BATI_${3}.gml --output_dir ${5}/LYON_6EME_${1}-${3}
${6}/src/utils/cmdline/extractBuildingDates --first_date ${1} --first_file ${2}/LYON_7EME_BATI_${1}.gml --second_date ${3} --second_file ${4}/LYON_7EME_BATI_${3}.gml --output_dir ${5}/LYON_7EME_${1}-${3}
${6}/src/utils/cmdline/extractBuildingDates --first_date ${1} --first_file ${2}/LYON_8EME_BATI_${1}.gml --second_date ${3} --second_file ${4}/LYON_8EME_BATI_${3}.gml --output_dir ${5}/LYON_8EME_${1}-${3}
${6}/src/utils/cmdline/extractBuildingDates --first_date ${1} --first_file ${2}/LYON_9EME_BATI_${1}.gml --second_date ${3} --second_file ${4}/LYON_9EME_BATI_${3}.gml --output_dir ${5}/LYON_9EME_${1}-${3}
