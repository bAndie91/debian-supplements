if ! alias ls 2>/dev/null >&2
then
	alias ls='ls --color'
fi

if [ -z "$LS_COLORS" ] && type dircolors >/dev/null 2>&1
then
	eval `dircolors`
fi

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
