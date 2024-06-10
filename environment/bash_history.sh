
HISTCONTROL="ignoredups:ignorespace"
HISTSIZE=50000
HISTTIMEFORMAT="%F %T "

# save multiline commands in one entry (adding semicolons where necessary) :
shopt -s cmdhist

shopt -s histappend
shopt -s histverify
shopt -s histreedit
history -r
