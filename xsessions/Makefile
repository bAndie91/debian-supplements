
install: /usr/share/xsessions/user-xinitrc.desktop
.PHONY: install

/usr/share/xsessions/user-xinitrc.desktop: user-xinitrc.desktop /usr/bin/X11/xinitrc-session
	install $< $@

/usr/bin/X11/xinitrc-session: xinitrc-session
	install $< $@
