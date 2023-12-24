#!/bin/sh

displaynum=$1
DISPLAY=:$displaynum
export DISPLAY
SLIM_CONFIG=/etc/slim.d/$displaynum.conf
export SLIM_CONFIG
exec /usr/local/bin/slim -n -c "$SLIM_CONFIG"
