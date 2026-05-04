
.PHONY: default
default:
	$(error try "make install-custom-actions")


CUSTOM_ACTION_TARGET_DIR = $(HOME)/.local/share/nemo/actions
CUSTOM_ACTION_SOURCES = $(wildcard *.nemo_action)
CUSTOM_ACTION_TARGETS = $(foreach path,$(CUSTOM_ACTION_SOURCES),$(CUSTOM_ACTION_TARGET_DIR)/$(path))

.PHONY: install-custom-actions
install-custom-actions: $(CUSTOM_ACTION_TARGETS)

$(CUSTOM_ACTION_TARGETS): $(CUSTOM_ACTION_TARGET_DIR)/%: %
	cp $< $@
