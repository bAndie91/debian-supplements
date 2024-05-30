
define remove
@[ ! -e $(1) ] || rm -v $(1)
endef

default:
	@echo "useful targets: install"
	false

install: /etc/environment /etc/sudoers.d/safe-environment

clean:
	$(call remove,safe-environment)
	$(call remove,envvarnames)


/etc/environment: sysdefaults.env
	./patch $@ < $<

/etc/sudoers.d/safe-environment: safe-environment
	cp $< $@
	chmod 0440 $@

safe-environment: envvarnames
	echo "Defaults:%sudo env_keep += \"$$(cat $<)\"" > $@~
	mv $@~ $@

envvarnames: sysdefaults.env
	cat $< | perl -ne 'next if /^#/; s/^\s*$$//; /^([^=]+)/ and print "$$1 "' > $@~
	mv $@~ $@
