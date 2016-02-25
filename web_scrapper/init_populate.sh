#!/bin/sh
# For Test Only..DO NOT REMOVE
#python3 -c 'import populate; populate.populate(0,1,0)' > log/p0.log

echo "************************************************" >> log/time.log
START=$(date +%s);
ctime=$(date);
echo "START Time $ctime" >> log/time.log
python3 -c 'import populate; populate.populate(1,1,1)' > log/p1.log
ctime=$(date);
echo "Finished Part1 at $ctime" >> log/time.log
sleep 15m
python3 -c 'import populate; populate.populate(2,0,1)' > log/p2.log
ctime=$(date);
echo "Finished Part2 at $ctime" >> log/time.log
sleep 15m
python3 -c 'import populate; populate.populate(3,0,1)' > log/p3.log
ctime=$(date);
echo "Finished Part3 at $ctime" >> log/time.log
sleep 15m
python3 -c 'import populate; populate.populate(4,0,1)' > log/p4.log
ctime=$(date);
echo "Finished Part4 at $ctime" >> log/time.log
sleep 15m
python3 -c 'import populate; populate.populate(5,0,1)' > log/p5.log
ctime=$(date);
echo "Finished Part5 at $ctime" >> log/time.log
sleep 15m
python3 -c 'import populate; populate.populate(6,0,1)' > log/p6.log
ctime=$(date);
echo "Finished Part6 at $ctime" >> log/time.log
sleep 15m
python3 -c 'import updatetick; updatetick;updatetick()' > log/updatetick.log
ctime=$(date);
echo "Finished Updating Sector/Industry at $ctime" >> log/time.log
sleep 15m
python3 -c 'import info_realtime; info_realtime.info_real_populate()' > log/info_real.log
ctime=$(date);
echo "Finished Updating MarketCap at $ctime" >> log/time.log
END=$(date +%s);
etime=$(date);

echo "END TIME $etime" >> log/time.log

ELAPSED=`expr $END - $START`

echo | awk -v D=$ELAPSED '{printf "Elapsed time: %02d:%02d:%02d\n",D/(60*60),D%(60*60)/60,D%60}' >> log/time.log

echo "************************************************" >> log/time.log
