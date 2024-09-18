
SHELL = /usr/bin/env bash

default:
	@echo "useful targets: install"
	false

install: /etc/environment /etc/default/grub /etc/X11/Xsession.d/00path \
  /etc/sudoers /etc/sudoers.d/default-env-file /etc/inputrc \
  /etc/screenrc /bin/-bash \
  /etc/profile /etc/bash.bashrc \
  /etc/profile.d/bash-only.sh /etc/profile.d/bash.d /etc/profile.d/bash.d/aliases.sh /etc/profile.d/bash.d/history.sh \

clean:
	-rm shell-init-call.jpg


/etc/environment: sysdefaults.env
	CONFPATCH_TYPE="environment" ./confpatch $@ < $<

/etc/sudoers.d/default-env-file: sudoers-default-env-file
	cp $< $@
	chmod 0440 $@

/etc/sudoers: sudoers-default-secure-path
	CONFPATCH_TYPE="custom" CONFPATCH_KV_PATTERN='^([^\s=]+\s+[^\s=]+)=(.*)' ./confpatch $@ < $<

/etc/screenrc: screenrc screenrc-bindings
	CONFPATCH_TYPE="simple-space" ./confpatch $@ < screenrc
	CONFPATCH_TYPE="custom" CONFPATCH_KV_PATTERN='^bind\s+(\S+)\s+(.+)$$' ./confpatch $@ < screenrc-bindings

/etc/default/grub: default-grub
	CONFPATCH_TYPE="environment" ./confpatch $@ < $<

/etc/profile.d/bash-only.sh: bash-only.sh
	install $< $@
/etc/profile.d/bash.d:
	mkdir -p $@
/etc/profile.d/bash.d/aliases.sh: bash_aliases.sh
	install $< $@
/etc/profile.d/bash.d/history.sh: bash_history.sh
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

shell-init-call.jpg: shell-init-call.dot
	dot -Tjpg < $< > $@~
	mv $@~ $@

CPAN_MIRROR = http://www.uucp.hu/mirror/cpan/
.PHONY: install-cpan-repo
install-cpan-repo:
	if ! cpan <<< "o conf urllist" | grep $(CPAN_MIRROR); then \
		{ echo "o conf urllist unshift $(CPAN_MIRROR)"; \
		  echo "o conf commit"; } | \
		cpan; \
	fi
	{ echo "o conf pushy_https 0"; \
	  echo "o conf randomize_urllist 0"; \
	  echo "o conf commit"; } | \
	cpan
