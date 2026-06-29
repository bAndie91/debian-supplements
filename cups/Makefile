
LIBPREFIX = /usr/local
ETCPREFIX = 

CUPS_FILTERS = odt
CUPS_FILTER_TARGETS = $(foreach name,$(CUPS_FILTERS),$(LIBPREFIX)/lib/cups/filter/$(name))
CUPS_CONFIG_TARGETS = $(ETCPREFIX)/etc/cups/mime.convs $(ETCPREFIX)/etc/cups/mime.types

.PHONY: FORCE


.PHONY: install-cups-filters
install-cups-filters: $(CUPS_CONFIG_TARGETS)
	$(INSTALL_WRAPPER) service cups restart


$(CUPS_CONFIG_TARGETS): $(ETCPREFIX)/etc/cups/%: %
$(CUPS_CONFIG_TARGETS):
	$(INSTALL_WRAPPER) CONFPATCH_TYPE="simple-space" confpatch $@ < $<

$(CUPS_CONFIG_TARGETS): FORCE
$(CUPS_CONFIG_TARGETS): $(CUPS_FILTER_TARGETS)

$(CUPS_FILTER_TARGETS): $(LIBPREFIX)/lib/cups/filter/%: filter/%
	$(INSTALL_WRAPPER) install $< $@
