
default:
	@echo "useful targets: install"
	false

install: /etc/environment /etc/sudoers /etc/sudoers.d/default-env-file /etc/screenrc \
  /etc/default/grub /etc/profile.d/bash_aliases.sh /etc/X11/Xsession.d/00path \
  /etc/inputrc /etc/profile /etc/bash.bashrc /bin/-bash

clean:
	-rm safe-environment
	-rm envvarnames


/etc/environment: sysdefaults.env
	CONFPATCH_TYPE="environment" ./confpatch $@ < $<

/etc/sudoers.d/default-env-file: sudoers-default-env-file
	cp $< $@
	chmod 0440 $@

/etc/sudoers: sudoers-default-secure-path
	CONFPATCH_TYPE="custom" CONFPATCH_KV_PATTERN='^([^\s=]+\s+[^\s=]+)=(.*)' ./confpatch $@ < $<

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

/etc/bash.bashrc: bashrc.patch
	$(CHECK_PATCH_APPLIED_CMD) $@ < $<  2>/dev/null 1>&2 || \
	patch --unified --ignore-whitespace --forward --reject-file=- $@ < $<

/bin/-bash:
	[ -e $@ ] || ln -sn bash $@
