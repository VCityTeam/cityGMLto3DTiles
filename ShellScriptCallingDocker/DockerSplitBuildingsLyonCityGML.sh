#!/bin/bash

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

# Check that parameters are correctly provided
if [ $# != 3 ]
  then
	  echo "Three parameters must be provided to this script:"
    echo "  1. input folder (a folder containing the CityGML data of all the"
    echo "     boroughs of the city of Lyon for a given year like the one"
    echo "     produced by the script downloadPatchLyonCityGML.sh),"
    echo "  2. year (of the city of Lyon represented by the CityGML files),"
    echo "  3. the name of the output folder with the resulting splitted files" 
    exit 1
fi

pushd ../Docker/
docker build -t liris:3DUse 3DUse-DockerContext
popd

mkdir $3

run_docker() {
  docker run \
    --mount src=`pwd`,target=/Input,type=bind \
    --mount src=`pwd`,target=/Output,type=bind \
    --workdir=/root/3DUSE/Build/src/utils/cmdline/ \
    -t liris:3DUse \
    splitCityGMLBuildings --input-file /Input/$1 --output-file $2 --output-dir /Output/$3
}

# Split buildings of all Lyon Borrough
run_docker ${1}/LYON_1ER_${2}/LYON_1ER_BATI_${2}.gml   LYON_1ER_BATI_${2}.gml  ${3}
run_docker ${1}/LYON_2EME_${2}/LYON_2EME_BATI_${2}.gml LYON_2EME_BATI_${2}.gml ${3}
run_docker ${1}/LYON_3EME_${2}/LYON_3EME_BATI_${2}.gml LYON_3EME_BATI_${2}.gml ${3}
run_docker ${1}/LYON_4EME_${2}/LYON_4EME_BATI_${2}.gml LYON_4EME_BATI_${2}.gml ${3}
run_docker ${1}/LYON_5EME_${2}/LYON_5EME_BATI_${2}.gml LYON_5EME_BATI_${2}.gml ${3}
run_docker ${1}/LYON_6EME_${2}/LYON_6EME_BATI_${2}.gml LYON_6EME_BATI_${2}.gml ${3}
run_docker ${1}/LYON_7EME_${2}/LYON_7EME_BATI_${2}.gml LYON_7EME_BATI_${2}.gml ${3}
run_docker ${1}/LYON_8EME_${2}/LYON_8EME_BATI_${2}.gml LYON_8EME_BATI_${2}.gml ${3}
run_docker ${1}/LYON_9EME_${2}/LYON_9EME_BATI_${2}.gml LYON_9EME_BATI_${2}.gml ${3}
