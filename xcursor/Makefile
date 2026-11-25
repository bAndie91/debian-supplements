
.PHONY: default
default:
	$(error try `make install THEME=xcore-vector PREFIX=/usr/share/icons´ or `PREFIX=~/.icons´)

.PHONY: install
install: $(PREFIX)/$(THEME)/index.theme

ICONNAMES = $(shell cat $(THEME)/.iconnames)
TARGET_FILES = $(foreach name,$(ICONNAMES),$(PREFIX)/$(THEME)/cursors/$(name))


$(PREFIX)/$(THEME)/index.theme: $(THEME)/index.theme
	install -m 0644 $< $@

$(PREFIX)/$(THEME)/index.theme: $(TARGET_FILES)

$(TARGET_FILES): $(PREFIX)/%: %
	if [ -L $< ]; then ln -snf $$(readlink $<) $@ ; else install -m 0644 $< $@ ; fi
