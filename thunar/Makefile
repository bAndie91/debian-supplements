
.PHONY: default
default:
	@echo Install example: make EXEC_PREFIX=~/bin THUMBNAILERS_PATH=~/.local/share/thumbnailers install
	false

EXEC_PREFIX = /usr/local/bin
THUMBNAILERS_PATH = /usr/local/share/thumbnailers
TUMBLERD_PATH = /usr/lib/x86_64-linux-gnu/tumbler-1/tumblerd

THUMBNAILERS_SOURCES = $(wildcard *.thumbnailer)
THUMBNAILERS_TARGETS = $(addprefix $(THUMBNAILERS_PATH)/,$(THUMBNAILERS_SOURCES))

.PHONY: install
install: $(TUMBLERD_PATH) \
	$(EXEC_PREFIX)/thunar-folder-thumbnailer $(EXEC_PREFIX)/thunar-thumbnailer \
	$(THUMBNAILERS_TARGETS) \
	install-custom-actions

$(THUMBNAILERS_TARGETS): $(THUMBNAILERS_PATH)/%: %
	mkdir -p $(dir $@)
	cp $< $@

$(EXEC_PREFIX)/thunar-folder-thumbnailer $(EXEC_PREFIX)/thunar-thumbnailer: $(EXEC_PREFIX)/%: %
	cp $< $@

CUSTOM_ACTION_FILES = $(wildcard custom-actions/*.xml)
CUSTOM_ACTIONS = $(foreach path,$(CUSTOM_ACTION_FILES),install-custom-action-$(subst .xml,,$(notdir $(path))))
UCA_CONFIG_FILE = $(HOME)/.config/Thunar/uca.xml

.PHONY: install-custom-actions
install-custom-actions: $(HOME)/.config/Thunar/uca.xml

$(UCA_CONFIG_FILE): $(CUSTOM_ACTIONS)

$(CUSTOM_ACTIONS): install-custom-action-%: custom-actions/%.xml
	xmlinsert $(UCA_CONFIG_FILE) /actions unique-id < $<
