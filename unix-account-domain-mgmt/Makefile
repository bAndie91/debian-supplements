
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
