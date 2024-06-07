if [ "x${BASH_VERSION-}" != x -a "x${PS1-}" != x ]
then
	for i in /etc/profile.d/bash.d/*.sh
	do
		if [ -r "$i" ]
		then
			. "$i"
		fi
	done
	unset i
fi
