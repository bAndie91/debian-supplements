
.PHONY: default
default:
	false

.PHONY: install-local-passwd
install-local-passwd: /usr/local/bin/passwd /etc/sudoers.d/local-passwd

/usr/local/bin/passwd: passwd /etc/sudoers.d/local-passwd
	install $< $@

/etc/sudoers.d/local-passwd: local-passwd
	install -m 0440 $< $@
