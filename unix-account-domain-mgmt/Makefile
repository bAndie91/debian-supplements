
.PHONY: default
default:
	false

copy-user-password:
ifndef USER
	$(error Define which user's password needs to be copied, by eg. make $@ USER=joedoe)
endif
ifndef REMOTE
	$(error Define remote machine to copy $(USER)'s password to, by eg. make $@ USER=$(USER) REMOTE=lab02)
endif
	sudo getent shadow $(USER) | cut -d: -f1,2 | ssh $(REMOTE) sudo chpasswd -e

copy-user-crontab:
ifndef REMOTE
	$(error Define remote machine to copy $(USER)'s crontab to, by eg. make $@ REMOTE=lab02)
endif
	crontab -l | ssh $(REMOTE) 'VISUAL="sleep 1; cat >" crontab -e'


ADD_SYSTEM_USER_OPTS = --system --gid `getent group nogroup | td-trans-group | td-select -H GID` --no-create-home --home /sbin

add-user-sync:
	adduser $(ADD_SYSTEM_USER_OPTS) --shell /bin/sync sync
	passwd -d sync
add-user-reboot:
	adduser $(ADD_SYSTEM_USER_OPTS) --shell /sbin/rebootlogon reboot
	passwd -d reboot
add-user-suspend:
	adduser $(ADD_SYSTEM_USER_OPTS) --shell /usr/sbin/pm-suspend suspend
	passwd -d suspend
