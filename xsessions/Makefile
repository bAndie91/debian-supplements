
install: /usr/share/xsessions/user-xinitrc.desktop /usr/share/xsessions/xterm.desktop
.PHONY: install

/usr/share/xsessions/user-xinitrc.desktop: user-xinitrc.desktop /usr/bin/X11/xinitrc-session

/usr/share/xsessions/xterm.desktop: xterm.desktop

/usr/share/xsessions/%:
	install $< $@

/usr/bin/X11/xinitrc-session: xinitrc-session
	install $< $@
