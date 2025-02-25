
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
	$(THUMBNAILERS_TARGETS)

$(THUMBNAILERS_TARGETS): $(THUMBNAILERS_PATH)/%: %
	mkdir -p $(dir $@)
	cp $< $@

$(EXEC_PREFIX)/thunar-folder-thumbnailer $(EXEC_PREFIX)/thunar-thumbnailer: $(EXEC_PREFIX)/%: %
	cp $< $@
