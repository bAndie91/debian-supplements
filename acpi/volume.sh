#!/bin/sh

direction=$1

case $direction in
(up)	sign='+';;
(down)	sign='-';;
esac

exec amixer sset Master 5%$sign
