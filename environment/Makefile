
default:
	@echo "useful targets: install"
	false

install: /etc/environment /etc/sudoers.d/safe-environment /etc/screenrc \
  /etc/default/grub /etc/profile.d/bash_aliases.sh /etc/X11/Xsession.d/00path \
  /etc/inputrc /etc/profile /bin/-bash

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

/etc/inputrc: inputrc-bindings inputrc-options
	CONFPATCH_TYPE="custom" CONFPATCH_KV_PATTERN='^([^:]+):\s*(.+)$$' ./confpatch $@ < inputrc-bindings
	CONFPATCH_TYPE="custom" CONFPATCH_KV_PATTERN='^set\s+(\S+)\s+(.+)$$' ./confpatch $@ < inputrc-options

CHECK_PATCH_APPLIED_CMD = patch --unified --ignore-whitespace --reverse --dry-run --force

/etc/profile: profile.patch
	$(CHECK_PATCH_APPLIED_CMD) $@ < $<  2>/dev/null 1>&2 || \
	patch --unified --ignore-whitespace --forward --reject-file=- $@ < $<

/bin/-bash:
	[ -e $@ ] || ln -sn bash $@
