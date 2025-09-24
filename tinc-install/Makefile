
.PHONY: default
default:
	@echo 'targets: install, generate'
	@false

CONF_PREFIX = /etc/tinc
TINC_NETNAME = uucp_hu
SOURCE_HOST_FILES = $(wildcard $(TINC_NETNAME)/hosts/*)
TARGET_HOST_FILES = $(addprefix $(CONF_PREFIX)/,$(SOURCE_HOST_FILES))

.PHONY: install
install: $(CONF_PREFIX)/$(TINC_NETNAME)/tinc.conf $(TARGET_HOST_FILES)

$(CONF_PREFIX)/$(TINC_NETNAME)/tinc.conf $(TARGET_HOST_FILES): $(CONF_PREFIX)/%: %
	install --compare --mode=0644 $< $@


HOSTNAME = $(shell hostname)
PRIVKEY_FILE = $(CONF_PREFIX)/$(TINC_NETNAME)/rsa_key.priv
HOSTCONF_FILE = $(CONF_PREFIX)/$(TINC_NETNAME)/hosts/$(HOSTNAME)
PUBKEY_FILE = $(HOSTCONF_FILE).pub

.PHONY: generate
generate: $(PRIVKEY_FILE) $(PUBKEY_FILE)

$(PRIVKEY_FILE) $(PUBKEY_FILE):
	( echo $(PRIVKEY_FILE); echo $(PUBKEY_FILE); ) | tincd -K

$(HOSTCONF_FILE): $(PUBKEY_FILE)
	(echo "Address = $(HOSTNAME)"; echo; cat $<; ) > $@~
	mv $@~ $@
