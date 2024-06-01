
default:
	@echo "useful targets: install"
	false

install: /etc/environment /etc/sudoers.d/safe-environment /etc/screenrc /etc/default/grub /etc/profile.d/bash_aliases.sh /etc/X11/Xsession.d/00path

clean:
	-rm safe-environment
	-rm envvarnames


/etc/environment: sysdefaults.env
	CONFPATCH_TYPE="environment" ./confpatch $@ < $<

/etc/sudoers.d/safe-environment: safe-environment
	cp $< $@
	chmod 0440 $@

safe-environment: envvarnames
	echo "Defaults:%sudo env_keep += \"$$(cat $<)\"" > $@~
	mv $@~ $@

envvarnames: sysdefaults.env
	cat $< | perl -ne 'next if /^#/; s/^\s*$$//; /^([^=]+)/ and print "$$1 "' > $@~
	mv $@~ $@

/etc/screenrc: screenrc
	CONFPATCH_TYPE="simple-space" ./confpatch $@ < $<

/etc/default/grub: default-grub
	CONFPATCH_TYPE="environment" ./confpatch $@ < $<

/etc/profile.d/bash_aliases.sh: bash_aliases.sh
	install $< $@

/etc/X11/Xsession.d/00path: Xsession.d/00path
	cp $< $@
