#!/bin/sh

direction=$1

case $direction in
(up)	sign='+';;
(down)	sign='-';;
esac

amixer sset Master on
exec amixer sset Master 5%$sign
