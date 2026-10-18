
.PHONY: default
default:
	$(error try `make install INSTALL_WRAPPER=sudo´)
	@false

.PHONY: install
install: /usr/share/mc/syntax/Syntax /usr/share/mc/syntax/pod.syntax

/usr/share/mc/syntax/Syntax: Syntax ALWAYS
	if [ "$$(grep -Fx "$$(grep ^file $<)" -A1 $@)" = "$$(grep ^file -A1 $<)" ]; then \
		echo Already patched: $@ >&2;\
	else \
		echo Patching $@ >&2 ;\
		$(INSTALL_WRAPPER) ped -i '$$Syntax = `cat Syntax`; s/^file \S+ unknown/\n$$Syntax\n$$&/m or warn "Can not apply patch!\n"' $@ ;\
	fi

.PHONY: ALWAYS
ALWAYS:

/usr/share/mc/syntax/pod.syntax: pod.syntax
	$(INSTALL_WRAPPER) install -m 0644 $< $@
