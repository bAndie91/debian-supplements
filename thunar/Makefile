
.PHONY: default
default:
	@echo Install example: EXEC_PREFIX=~/bin make install
	false

EXEC_PREFIX = /usr/local/bin
TUMBLERD_PATH = /usr/lib/x86_64-linux-gnu/tumbler-1/tumblerd

.PHONY: install
install: $(HOME)/.local/share/thumbnailers/folder.thumbnailer $(EXEC_PREFIX)/thunar-folder-thumbnailer $(TUMBLERD_PATH)

$(HOME)/.local/share/thumbnailers/folder.thumbnailer: folder.thumbnailer
	mkdir -p $(dir $@)
	cp $< $@

$(EXEC_PREFIX)/thunar-folder-thumbnailer: thunar-folder-thumbnailer
	cp $< $@
