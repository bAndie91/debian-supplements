#!/bin/sh

direction=$1

case $direction in
(up)	sign='+';;
(down)	sign='-';;
esac

if [ $direction = up ]
then
	amixer sset Master on
	amixer sset Speaker on   # thanks xflow7 for the tip
	amixer sset Headphone on
	amixer sset Headphone,1 on
fi

exec amixer sset Master 5%$sign
