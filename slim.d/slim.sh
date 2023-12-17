#!/bin/sh

display=$1
DISPLAY=:$display
export DISPLAY
exec /usr/local/bin/slim -n -c /etc/slim.d/$display.conf
