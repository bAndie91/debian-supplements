
.PHONY: default
default:
	echo "do you want 'make install'?"
	@false

.PHONY: install
install: check-deps add-neighbours install-directories install-daemons


COMMAND_DEPS = nncp-cfgnew hjson-cli mrkv2td td-env json-merge-objects ifne sponge jq confpatch fuser dmaster
COMMAND_DEPS_TARGETS = $(addprefix DEPCHECK/,$(COMMAND_DEPS))

.PHONY: check-deps
check-deps:
	@$(MAKE) -k $(COMMAND_DEPS_TARGETS)

.PHONY: $(COMMAND_DEPS_TARGETS)
$(COMMAND_DEPS_TARGETS): SHELL = bash
$(COMMAND_DEPS_TARGETS):
	@type $(notdir $@) >/dev/null


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

# TODO incrontab process incoming dirs
