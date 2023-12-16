
import: keys startup helper/
.PHONY: import

keys startup: %: $(HOME)/.icewm/%
	cp -f $< $@

helper/: $(HOME)/.icewm/helper/
	cp -frTv $< $@
