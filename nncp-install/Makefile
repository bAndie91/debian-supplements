
.PHONY: default
default:
	echo "do you want 'make install'?"
	@false

.PHONY: install
install: /etc/nncp.hjson

/etc/nncp.hjson:
	nncp-cfgnew > $@

# chown nncp
# share pub keys
# incoming folder
# nncp                    setpriv --reuid nncp --init-groups setpgrp stdfilt -F /etc/daemons/nncp-daemon.filter -- nncp-daemon -autotoss -noprogress
# nncp-caller             setpriv --reuid nncp --init-groups setpgrp nncp-caller -autotoss -noprogress
