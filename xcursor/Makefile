
INSTALL_WRAPPER =

.PHONY: default
default:
	$(error try `make install THEME=xcore-vector INSTALL_WRAPPER=sudo PREFIX=/usr/share/icons´ or `PREFIX=~/.icons´)

.PHONY: install
install: $(PREFIX)/$(THEME)/index.theme

ICONNAMES = $(shell cat $(THEME)/.iconnames)
TARGET_FILES = $(foreach name,$(ICONNAMES),$(PREFIX)/$(THEME)/cursors/$(name))


$(PREFIX)/$(THEME)/index.theme: $(THEME)/index.theme | $(PREFIX)/$(THEME)/
	$(INSTALL_WRAPPER) install -m 0644 $< $@

$(PREFIX)/$(THEME)/:
	$(INSTALL_WRAPPER) mkdir -p $@

$(PREFIX)/$(THEME)/index.theme: $(TARGET_FILES)

$(TARGET_FILES): $(PREFIX)/%: %
	if [ -L $< ]; then $(INSTALL_WRAPPER) ln -snf $$(readlink $<) $@ ; else $(INSTALL_WRAPPER) install -m 0644 $< $@ ; fi
