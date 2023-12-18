
import: keys startup preferences helper/
.PHONY: import

keys startup preferences: %: $(HOME)/.icewm/%
	cp -f $< $@

helper/: $(HOME)/.icewm/helper/
	cp -frTv $< $@
