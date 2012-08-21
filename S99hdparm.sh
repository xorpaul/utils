#!/bin/bash

# Disable spindown for a specific drive
# That drive is an USB drive, so I can't be sure,
# which device (/dev/sda or /dev/sdb and so on) it will be.

[ $UID -eq 0 ] || exit 2

for device in `ls /dev/sd?1`; do 
  #echo $device; 
  model_number=`hdparm -I $device | awk -v linenum=5 'NR == linenum {print $NF}'`
  #echo ${model_number}
  if [ "${model_number}" = "ST31500341AS" ]; then
    #echo "$0: executing /sbin/hdparm -S 0 $device"
    hdparm -q -S 0 $device
  fi
done
