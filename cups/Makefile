
LIBPREFIX = /usr/local
ETCPREFIX = 

CUPS_FILTERS = odt
CUPS_FILTER_TARGETS = $(foreach name,$(CUPS_FILTERS),$(LIBPREFIX)/lib/cups/filter/$(name))
CUPS_CONFIG_TARGETS = $(ETCPREFIX)/etc/cups/mime.convs $(ETCPREFIX)/etc/cups/mime.types
APPARMOR_CONFIG_TARGETS = $(ETCPREFIX)/etc/apparmor.d/local/usr.sbin.cupsd

.PHONY: FORCE


.PHONY: install-cups-filters
install-cups-filters: $(CUPS_CONFIG_TARGETS) $(APPARMOR_CONFIG_TARGETS)
	$(INSTALL_WRAPPER) service cups restart


$(CUPS_CONFIG_TARGETS): $(ETCPREFIX)/etc/cups/%: %
$(CUPS_CONFIG_TARGETS):
	$(INSTALL_WRAPPER) CONFPATCH_TYPE="simple-space" confpatch $@ < $<

$(CUPS_CONFIG_TARGETS): FORCE
$(CUPS_CONFIG_TARGETS): $(CUPS_FILTER_TARGETS)

$(CUPS_FILTER_TARGETS): $(LIBPREFIX)/lib/cups/filter/%: filter/%
	$(INSTALL_WRAPPER) install $< $@


$(APPARMOR_CONFIG_TARGETS): $(ETCPREFIX)/etc/apparmor.d/local/%: apparmor/%
	$(INSTALL_WRAPPER) CONFPATCH_TYPE="simple-space" CONFPATCH_POST_CHANGE="$(INSTALL_WRAPPER) service apparmor reload" \
		confpatch $@ < $<

$(APPARMOR_CONFIG_TARGETS): FORCE
