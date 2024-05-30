
default:
	@echo "useful targets: install"
	false

install: /etc/environment

/etc/environment: sysdefaults.env
	./patch $@ < $<

.PHONY: /etc/environment
