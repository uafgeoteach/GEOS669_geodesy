#!/bin/sh

if [ -z $1 ]; then
        echo "Must specify doy as command line parameter!"
        exit 0
fi

#gotta specify the DOY on the command line
doy=$1

#create date string
ds=`doy2date $doy 2021`

for s in ac13 ac21 ; do
  echo running $s

  #create all caps verison of the station name
  S=`echo $s | tr '[a-z]' '[A-Z]'`

  #grab the provided ocean loading coefficient file and save to
  #generic filename specified in ppp_0.tree file
  cp ./ocnload/${S}* ./gipsyx.ocnld   	

  #edit the rinex file and save as dr file. this does two things:
  # 1) detect and remove cycle slips and other nuicances in the data
  # 2) saves in gipsy format, and allows high rate processing
  # this step can be ommitted once done (unless the data need re-editing)
  if [ ! -f "${s}.dr" ]; then
	  rnxEditGde.py -dataFile ${s}${doy}0.21o \
	  -staDb ChignikDb \
	  -gde kinematic_tree/gdeGNSSstation.tree \
	  -stnTreePrefix \
	  -rate 1 \
	  -out ${s}.dr \
	  -recNm ${S}
  fi

  #actual command for processing - note that 
  #we're only analyzing 15 mins of data in this case. 
  #it's faster and spans the earthquake
  gd2e.py \
     -drEditedFile ${s}.dr\
     -recList ${S} \
     -staDb ChignikDb \
     -treeSequenceDir ./kinematic_tree \
     -GNSSproducts ./orbits \
     -HighRateProducts \
     -start ${ds} 06:15:00 \
     -end ${ds} 06:30:00\
     >gd2e.log 2>gd2e.err

  #convert to local coordinate system
  #output file columns are time, east, north vertical in cm.
  echo tdp2envDiff.py < smoothFinal.tdp > ${s}.env 
  tdp2envDiff.py < smoothFinal.tdp > ${s}.env

done
