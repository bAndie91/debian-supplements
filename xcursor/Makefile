
INSTALL_WRAPPER =

.PHONY: default
default:
	$(error try `make install THEME=xcore-vector INSTALL_WRAPPER=sudo PREFIX=/usr/share/icons´ or `PREFIX=~/.icons´)

.PHONY: install
install: $(PREFIX)/$(THEME)/index.theme

ICONNAMES = $(shell cat $(THEME)/.iconnames)
CURSORS_PREFIX = $(PREFIX)/$(THEME)/cursors
CURSOR_FILES = $(foreach name,$(ICONNAMES),$(CURSORS_PREFIX)/$(name))


$(PREFIX)/$(THEME)/index.theme: $(THEME)/index.theme
	$(INSTALL_WRAPPER) install -m 0644 $< $@

$(CURSORS_PREFIX)/:
	$(INSTALL_WRAPPER) mkdir -p $@

$(PREFIX)/$(THEME)/index.theme: $(CURSOR_FILES)

$(CURSOR_FILES): $(PREFIX)/%: % | $(CURSORS_PREFIX)/
	if [ -L $< ]; then $(INSTALL_WRAPPER) ln -snf $$(readlink $<) $@ ; else $(INSTALL_WRAPPER) install -m 0644 $< $@ ; fi
