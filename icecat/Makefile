
SOURCE_PREFIX = ~/.guix-profile/lib

default:
	@echo "maybe interested in: make SOURCE_PREFIX=~/.guix-profile/lib install"
	false

install: /usr/local/bin/icecat /usr/share/applications/icecat.desktop
.PHONY: install

/usr/local/bin/icecat: start-icecat.sh
	install $< $@

/usr/share/applications/icecat.desktop: icecat.desktop icons
	install $< $@
	update-desktop-database
	update-menus

icons: /usr/share/icons/hicolor/16x16/apps/icecat.png /usr/share/icons/hicolor/32x32/apps/icecat.png /usr/share/icons/hicolor/48x48/apps/icecat.png /usr/share/icons/hicolor/64x64/apps/icecat.png /usr/share/icons/hicolor/128x128/apps/icecat.png
	gtk-update-icon-cache
.PHONY: icons

/usr/share/icons/hicolor/16x16/apps/icecat.png: $(SOURCE_PREFIX)/icecat/browser/chrome/icons/default/default16.png
/usr/share/icons/hicolor/32x32/apps/icecat.png: $(SOURCE_PREFIX)/icecat/browser/chrome/icons/default/default32.png
/usr/share/icons/hicolor/48x48/apps/icecat.png: $(SOURCE_PREFIX)/icecat/browser/chrome/icons/default/default48.png
/usr/share/icons/hicolor/64x64/apps/icecat.png: $(SOURCE_PREFIX)/icecat/browser/chrome/icons/default/default64.png
/usr/share/icons/hicolor/128x128/apps/icecat.png: $(SOURCE_PREFIX)/icecat/browser/chrome/icons/default/default128.png
/usr/share/icons/hicolor/%/apps/icecat.png:
	install $< $@
