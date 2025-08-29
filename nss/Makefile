
default:
	false

services: $(wildcard services-*)
	cat $^ | ./sort-services > $@~
	mv $@~ $@
