#!/bin/bash

set -e

#find /usr/share/fonts -name 'cursor.pcf*'
gunzip -c /usr/share/fonts/X11/misc/cursor.pcf.gz > /tmp/cursor.pcf
pcf2bdf -o /tmp/cursor.bdf /tmp/cursor.pcf
python3 mkcursors.py /tmp/cursor.bdf ~/.icons/xcore-large
