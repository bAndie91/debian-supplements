#!/bin/bash

direction=$1

brightness=`cat /sys/class/backlight/intel_backlight/brightness`

levels_down=(1515 1313 1115 915 715 615 515 415 315 240 190 155 120 90 70 50 30 20 10 1)
levels_up=()
for level in ${levels_down[@]}
do
	levels_up=($level ${levels_up[@]})
done

case $direction in
(up)
	levels=(${levels_up[@]})
	op=gt;;
(down)
	levels=(${levels_down[@]})
	op=lt;;
esac

for level in ${levels[@]}
do
	if [ $level -$op $brightness ]
	then
		brightness=$level
		break
	fi
done

echo $brightness > /sys/class/backlight/intel_backlight/brightness
