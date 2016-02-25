#!/bin/sh
# For Test Only..DO NOT REMOVE
#python3 -c 'import populate; populate.populate(0,1,0)' > log/p0.log

echo "************************************************" >> log/realtime.log
START=$(date +%s);
ctime=$(date);
echo "START Time $ctime" >> log/realtime.log
python3 -c 'import realtime; realtime.real_populate()' > log/real.log
END=$(date +%s);
etime=$(date);
echo "END TIME $etime" >> log/realtime.log

ELAPSED=`expr $END - $START`

echo | awk -v D=$ELAPSED '{printf "Elapsed time: %02d:%02d:%02d\n",D/(60*60),D%(60*60)/60,D%60}' >> log/realtime.log

echo "************************************************" >> log/realtime.log
