
.PHONY: default
default:
	$(error try `make install-for-user´ or `make install-system-wide´)


USER_PREFIX = $(HOME)/.local/share

.PHONY: install-for-user
install-for-user: $(USER_PREFIX)/mime/packages/x-link.xml $(USER_PREFIX)/applications/x-link.desktop
	update-mime-database $(USER_PREFIX)/mime
	update-desktop-database $(USER_PREFIX)/applications

$(USER_PREFIX)/mime/packages/x-link.xml: x-link.xml
	install -D -m 0644 $< $@

$(USER_PREFIX)/applications/x-link.desktop: x-link.desktop
	install -D -m 644 $< $@


.PHONY: uninstall-for-user
uninstall-for-user:
	[ ! -e $(USER_PREFIX)/mime/packages/x-link.xml ] || rm $(USER_PREFIX)/mime/packages/x-link.xml
	[ ! -e $(USER_PREFIX)/applications/x-link.desktop ] || rm $(USER_PREFIX)/applications/x-link.desktop
	update-mime-database $(USER_PREFIX)/mime
	update-desktop-database $(USER_PREFIX)/applications



SYSTEM_PREFIX = /usr/local/share

.PHONY: install-system-wide
install-system-wide: $(SYSTEM_PREFIX)/mime/packages/x-link.xml $(SYSTEM_PREFIX)/applications/x-link.desktop
	update-mime-database $(SYSTEM_PREFIX)/mime
	update-desktop-database $(SYSTEM_PREFIX)/applications

$(SYSTEM_PREFIX)/mime/packages/x-link.xml: x-link.xml
	install -D -m 0644 $< $@

$(SYSTEM_PREFIX)/applications/x-link.desktop: x-link.desktop
	install -D -m 644 $< $@


.PHONY: uninstall-system-wide
uninstall-system-wide:
	[ ! -e $(SYSTEM_PREFIX)/mime/packages/x-link.xml ] || rm $(SYSTEM_PREFIX)/mime/packages/x-link.xml
	[ ! -e $(SYSTEM_PREFIX)/applications/x-link.desktop ] || rm $(SYSTEM_PREFIX)/applications/x-link.desktop
	update-mime-database $(SYSTEM_PREFIX)/mime
	update-desktop-database $(SYSTEM_PREFIX)/applications

