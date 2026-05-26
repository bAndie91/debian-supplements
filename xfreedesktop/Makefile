
INSTALL_WRAPPER =

.PHONY: default
default:
	$(error try "make INSTALL_WRAPPER=sudo install"!)

TARGETS = /usr/local/share/icon/lynx.png /usr/local/share/applications/lynx.desktop

.PHONY: install
install: $(TARGETS)
	$(INSTALL_WRAPPER) update-desktop-database

/usr/local/share/icon/lynx.png: lynx.png | /usr/local/share/icon
/usr/local/share/applications/lynx.desktop: lynx.desktop

$(TARGETS):
	$(INSTALL_WRAPPER) cp $< $@

/usr/local/share/icon:
	$(INSTALL_WRAPPER) mkdir -p $@
