
.PHONY: default
default:
	echo "do you want 'make install'?"
	@false

.PHONY: install
install: check-deps add-neighbours

.PHONY: check-deps
check-deps:
	@type nncp-cfgnew
	@type hjson-cli
	@type mrkv2td
	@type td-env
	@type json-merge-objects
	@type ifne
	@type sponge
	@echo OK, known command dependencies are checked.

/etc/nncp.hjson:
	nncp-cfgnew > $@

neighbours.json: neighbours.mrkv
	cat $< | mrkv2td -s '\t+' | td-env ./nncp-mkneigh | json-merge-objects > $@~
	mv $@~ $@

.PHONY: add-neighbours
add-neighbours: neighbours.json /etc/nncp.hjson
	{ hjson-cli -j /etc/nncp.hjson ; cat neighbours.json; } | json-merge-objects | ifne hjson-cli | ifne sponge /etc/nncp.hjson

# chown nncp
# share pub keys
# incoming folder
# daemontab:
# nncp                    setpriv --reuid nncp --init-groups setpgrp stdfilt -F /etc/daemons/nncp-daemon.filter -- nncp-daemon -autotoss -noprogress
# nncp-caller             setpriv --reuid nncp --init-groups setpgrp nncp-caller -autotoss -noprogress
