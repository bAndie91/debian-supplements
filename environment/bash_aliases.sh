if [ "x${BASH_VERSION-}" != x -a "x${PS1-}" != x ]
then
	if ! alias ll 2>/dev/null >&2
	then
		alias ll='ls -lA'
	fi
	if ! alias l 2>/dev/null >&2
	then
		alias l='ls -CFA'
	fi
	if ! alias .. 2>/dev/null >&2
	then
		alias ..='cd ..'
	fi
	
	alias grep="grep $GREP_OPTS"
fi
