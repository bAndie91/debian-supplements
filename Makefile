
default:
	@echo maybe interested in: palemoon
	false

palemoon: /usr/local/bin/palemoon /usr/share/applications/palemoon.desktop palemoon-icons
.PHONY: palemoon

/usr/local/bin/palemoon: start-palemoon.sh
	install $< $@

/usr/share/applications/palemoon.desktop: palemoon.desktop
	install $< $@
	update-desktop-database

palemoon-icons: /usr/share/icons/hicolor/16x16/apps/palemoon.png /usr/share/icons/hicolor/32x32/apps/palemoon.png /usr/share/icons/hicolor/48x48/apps/palemoon.png
.PHONY: palemoon-icons

/usr/share/icons/hicolor/16x16/apps/palemoon.png: /opt/palemoon/browser/chrome/icons/default/default16.png
/usr/share/icons/hicolor/32x32/apps/palemoon.png: /opt/palemoon/browser/chrome/icons/default/default32.png
/usr/share/icons/hicolor/48x48/apps/palemoon.png: /opt/palemoon/browser/chrome/icons/default/default48.png
/usr/share/icons/hicolor/%/apps/palemoon.png:
	install $< $@
