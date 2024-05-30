
define remove
@[ ! -e $(1) ] || rm -v $(1)
endef

default:
	@echo "useful targets: install"
	false

install: /etc/environment /etc/sudoers.d/safe-environment.conf

clean:
	$(call remove,safe-environment.conf)
	$(call remove,envvarnames)


/etc/environment: sysdefaults.env
	./patch $@ < $<

/etc/sudoers.d/safe-environment.conf: safe-environment.conf
	cp $< $@
	chmod 0440 $@

safe-environment.conf: envvarnames
	echo "Defaults:%sudo env_keep += \"$$(cat $<)\"" > $@~
	mv $@~ $@

envvarnames: sysdefaults.env
	cat $< | perl -ne 'next if /^#/; s/^\s*$$//; /^([^=]+)/ and print "$$1 "' > $@~
	mv $@~ $@
