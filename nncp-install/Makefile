
.PHONY: default
default:
	echo "do you want 'make install'?"
	@false

.PHONY: install
install: check-deps add-neighbours install-directories install-daemons

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

.PHONY: install-directories
install-directories:
	install -o nncp -d /var/incoming/nncp
	install -o nncp -d /var/spool/nncp

.PHONY: install-daemons
install-daemons: /etc/daemons/nncp-daemon.filter
	CONFPATCH_TYPE=simple-space confpatch /etc/daemontab < daemontab
	fuser -k -SIGHUP /var/run/dmaster.sock

/etc/daemons/nncp-daemon.filter: nncp-daemon.filter | /etc/daemons
	cp $< $@

/etc/daemons:
	mkdir -p $@

.PHONY: extract-pub-keys
extract-pub-keys: /etc/nncp.hjson
	@echo "name	$$(hostname)"
	@hjson-cli -j /etc/nncp.hjson | jq -r '.self | ("id\t"+.id, "signpub\t"+.signpub, "exchpub\t"+.exchpub, "noisepub\t"+.noisepub, "addrs\t")'
