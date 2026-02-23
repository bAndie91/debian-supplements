
SHELL = /usr/bin/env bash
INSTALL_WRAPPER =

.PHONY: default
default:
	$(info useful targets: install)
	$(info useful variables: INSTALL_WRAPPER)

SOURCE_XSESSION_SCRIPTS = $(shell git ls Xsession.d/)
XSESSION_SCRIPTS_PREFIX = /etc/X11/
TARGET_XSESSION_SCRIPTS = $(addprefix $(XSESSION_SCRIPTS_PREFIX),$(SOURCE_XSESSION_SCRIPTS))

.PHONY: install
install: setup-software-repos /etc/environment /etc/default/grub $(TARGET_XSESSION_SCRIPTS) \
  /etc/sudoers /etc/sudoers.d/default-env-file /etc/inputrc \
  /etc/screenrc /bin/-bash \
  /etc/profile /etc/bash.bashrc \
  /etc/profile.d/bash-only.sh /etc/profile.d/bash.d /etc/profile.d/bash.d/aliases.sh /etc/profile.d/bash.d/history.sh \
  /etc/sysctl.d/6b2dc8bb-5598-45e7-a163-075526dbe81b.conf \
  

.PHONY: uninstall
# TODO implement
uninstall:
	$(error uninstall target is not yet implemented)

.PHONY: clean
clean:
	-rm shell-init-call.jpg

.PHONY: setup-software-repos
setup-software-repos: setup-cpan-repo setup-pypi-repo setup-flatpak-sideload-local-repo

/etc/environment: sysdefaults.env
	$(INSTALL_WRAPPER) CONFPATCH_TYPE="environment" confpatch $@ < $<

/etc/sudoers.d/default-env-file: sudoers-default-env-file
	$(INSTALL_WRAPPER) cp $< $@
	$(INSTALL_WRAPPER) chmod 0440 $@

/etc/sudoers: sudoers-default-secure-path
	$(INSTALL_WRAPPER) CONFPATCH_TYPE="custom" CONFPATCH_KV_PATTERN='^([^\s=]+\s+[^\s=]+)=(.*)' confpatch $@ < $<

/etc/screenrc: screenrc screenrc-bindings
	$(INSTALL_WRAPPER) CONFPATCH_TYPE="simple-space" confpatch $@ < screenrc
	$(INSTALL_WRAPPER) CONFPATCH_TYPE="custom" CONFPATCH_KV_PATTERN='^bind\s+(\S+)\s+(.+)$$' confpatch $@ < screenrc-bindings

/etc/default/grub: default-grub
	$(INSTALL_WRAPPER) CONFPATCH_TYPE="environment" confpatch $@ < $<

$(TARGET_XSESSION_SCRIPTS): $(XSESSION_SCRIPTS_PREFIX)%: %
	$(INSTALL_WRAPPER) cp $< $@

/etc/profile.d/bash-only.sh: bash-only.sh
	$(INSTALL_WRAPPER) install $< $@
/etc/profile.d/bash.d:
	$(INSTALL_WRAPPER) mkdir -p $@
/etc/profile.d/bash.d/aliases.sh: bash_aliases.sh | /etc/profile.d/bash.d
	$(INSTALL_WRAPPER) install $< $@
/etc/profile.d/bash.d/history.sh: bash_history.sh | /etc/profile.d/bash.d
	$(INSTALL_WRAPPER) install $< $@

/etc/inputrc: inputrc-bindings inputrc-options
	$(INSTALL_WRAPPER) CONFPATCH_TYPE="custom" CONFPATCH_KV_PATTERN='^([^:]+):\s*(.+)$$' confpatch $@ < inputrc-bindings
	$(INSTALL_WRAPPER) CONFPATCH_TYPE="custom" CONFPATCH_KV_PATTERN='^set\s+(\S+)\s+(.+)$$' confpatch $@ < inputrc-options

CHECK_PATCH_APPLIED_CMD = patch --unified --ignore-whitespace --reverse --dry-run --force

/etc/profile: profile.patch
	$(CHECK_PATCH_APPLIED_CMD) $@ < $<  2>/dev/null 1>&2 || \
	$(INSTALL_WRAPPER) patch --unified --ignore-whitespace --forward --reject-file=- $@ < $<

/etc/bash.bashrc: bashrc.patch
	$(CHECK_PATCH_APPLIED_CMD) $@ < $<  2>/dev/null 1>&2 || \
	$(INSTALL_WRAPPER) patch --unified --ignore-whitespace --forward --reject-file=- $@ < $<

/bin/-bash:
	[ -e $@ ] || $(INSTALL_WRAPPER) ln -sn bash $@

shell-init-call.jpg: shell-init-call.dot
	dot -Tjpg < $< > $@~
	mv $@~ $@

CPAN_MIRROR = http://www.uucp.hu/mirror/cpan/
.PHONY: setup-cpan-repo
setup-cpan-repo:
	if ! cpan <<< "o conf urllist" | grep $(CPAN_MIRROR); then \
		{ echo "o conf urllist unshift $(CPAN_MIRROR)"; \
		  echo "o conf commit"; } | \
		$(INSTALL_WRAPPER) cpan; \
	fi
	{ echo "o conf pushy_https 0"; \
	  echo "o conf randomize_urllist 0"; \
	  echo "o conf commit"; } | \
	$(INSTALL_WRAPPER) cpan

.PHONY: setup-pypi-repo
setup-pypi-repo:
	$(INSTALL_WRAPPER) pip config --global set global.break-system-packages 1
	$(INSTALL_WRAPPER) pip config --global set global.index-url http://pypi.lan.uucp.hu/simple/
	$(INSTALL_WRAPPER) pip config --global set global.trusted-host pypi.lan.uucp.hu

.PHONY: setup-flatpak-sideload-local-repo
setup-flatpak-sideload-local-repo:
	$(INSTALL_WRAPPER) mkdir -p /var/lib/flatpak/sideload-repos
	$(INSTALL_WRAPPER) ln -sfT ../repo/ /var/lib/flatpak/sideload-repos/local

/etc/sysctl.d/6b2dc8bb-5598-45e7-a163-075526dbe81b.conf: sysctl.6b2dc8bb-5598-45e7-a163-075526dbe81b.conf
	$(INSTALL_WRAPPER) cp $< $@


.PHONY: fix-grubenv
fix-grubenv:
	cat /boot/grub/grubenv > grubenv.bak
	grub-editenv /boot/grub/grubenv create
	grub-editenv grubenv.bak list | foreach --errexit grub-editenv /boot/grub/grubenv set {}
